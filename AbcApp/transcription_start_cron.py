from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas
from azure.storage.blob import AccountSasPermissions
from AbcApp.micro_sentiment import inferencing, count
from AbcApp.call_quality import qa_main
from AbcApp.call_quality_hindi import qa_main_hindi
from AbcApp.media_to_storage import upload_file_to_azure
from azure.storage.blob import BlobServiceClient
from AbcApp import read_data_from_blob_cron
import logging
import requests
import time
import swagger_client as cris_client
import json
import sys
import os
import django
import traceback
from multiprocessing import Process

from django.utils import timezone

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")

sys.path.append("/".join(os.getcwd().replace("\\", "/").split("/")[0:-1]))
os.environ['DJANGO_SETTINGS_MODULE'] = 'ABC.settings'
django.setup()

from ABC.settings import BASE_DIR
from AbcApp.models import Analytic, CurrentProcessLog
global final_json

ACCOUNT_NAME = "absliamcsstoragemlai1"
ACCOUNT_KEY = "RECLddq51PeKWQ8mnsTmCLjtdFEtCoCSDIU0AL9BFt0jydaht/QqpcpT8wDJh//Zi1o7tCsu6XcyMZuIrEyl5g=="
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=absliamcsstoragemlai1;AccountKey=RECLddq51PeKWQ8mnsTmCLjtdFEtCoCSDIU0AL9BFt0jydaht/QqpcpT8wDJh//Zi1o7tCsu6XcyMZuIrEyl5g==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "ubonadata-storage"
LANGUAGE = {"english": "en-IN", "hindi": "hi-IN"}
SUBSCRIPTION_KEY = "810cb01716704bfe99f9c40121352750"
SERVICE_REGION = "centralindia"

NAME = "Simple transcription"
DESCRIPTION = "Simple transcription description"

# Set subscription information when doing transcription with custom models
ADAPTED_ACOUSTIC_ID = None  # guid of a custom acoustic model
ADAPTED_LANGUAGE_ID = None  # guid of a custom language model

#transcription starts
def get_conversation(json_file_path, txt_file_path):
    is_converted = False
    try:
        with open(json_file_path, 'r', encoding="utf-8") as f:
            parsed_response = json.load(f)

        print("Json file read successfully.")
        # json_data = parsed_response['AudioFileResults'][0]['SegmentResults']

        json_data = parsed_response['recognizedPhrases']

        with open(txt_file_path, "w", encoding="utf-8") as text_file:
            for speaker in json_data:
                if "speaker" in speaker.keys():
                    if speaker['speaker'] == 2:
                        text_file.write("S2 : " + speaker['nBest'][0]['display'] + '\n')
                    if speaker['speaker'] == 1:
                        text_file.write("S1 : " + speaker['nBest'][0]['display'] + '\n')
                    if speaker['speaker'] == 3:
                        text_file.write("S3 : " + speaker['nBest'][0]['display'] + '\n')
                    if speaker['speaker'] == 4:
                        text_file.write("S4 : " + speaker['nBest'][0]['display'] + '\n')
                    if speaker['speaker'] == 5:
                        text_file.write("S5 : " + speaker['nBest'][0]['display'] + '\n')

                else:
                    text_file.write("S1 : " + speaker['nBest'][0]['display'] + '\n')
        print("Text file written successfully.")
        text_file.close()
        is_converted = True
    except Exception as e:
        print("Error: Exception raised in get_conversation(). {0}".format(e))
        is_converted = False
    return is_converted


def get_public_url_of_blob(blob_name):
    account_name = ACCOUNT_NAME
    container_name = CONTAINER_NAME
    blob_name = blob_name
    account_key = ACCOUNT_KEY
    url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}"
    sas_token = generate_blob_sas(
        account_name=account_name,
        account_key=account_key,
        container_name=container_name,
        blob_name=blob_name,
        permission=AccountSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )

    source_url_with_sas = f"{url}?{sas_token}"
    return source_url_with_sas


def delete_all_transcriptions(api):
    """
    Delete all transcriptions associated with your speech resource.
    """
    logging.info("Deleting all existing completed transcriptions.")

    # get all transcriptions for the subscription
    transcriptions = list(_paginate(api, api.get_transcriptions()))

    # Delete all pre-existing completed transcriptions.
    # If transcriptions are still running or not started, they will not be deleted.
    for transcription in transcriptions:
        transcription_id = transcription._self.split('/')[-1]
        logging.debug(f"Deleting transcription with id {transcription_id}")
        try:
            api.delete_transcription(transcription_id)
        except cris_client.rest.ApiException as exc:
            logging.error(f"Could not delete transcription {transcription_id}: {exc}")


def _paginate(api, paginated_object):
    """
    The autogenerated client does not support pagination. This function returns a generator over
    all items of the array that the paginated object `paginated_object` is part of.
    """
    yield from paginated_object.values
    typename = type(paginated_object).__name__
    auth_settings = ["apiKeyHeader", "apiKeyQuery"]
    while paginated_object.next_link:
        link = paginated_object.next_link[len(api.api_client.configuration.host):]
        paginated_object, status, headers = api.api_client.call_api(link, "GET",
                                                                    response_type=typename, auth_settings=auth_settings)

        if status == 200:
            yield from paginated_object.values
        else:
            raise Exception(f"could not receive paginated data: status {status}")


def transcribe_from_single_blob(uri, properties, locale):
    """
    Transcribe a single audio file located at `uri` using the settings specified in `properties`
    using the base model for the specified locale.
    """
    transcription_definition = cris_client.Transcription(
        display_name=NAME,
        description=DESCRIPTION,
        locale=locale,
        content_urls=[uri],
        properties=properties
    )

    return transcription_definition


def update_status(request_id, status):
    try:
        get_db_record = Analytic.objects.get(request_id=request_id)
        get_db_record.transcription_status = status
        get_db_record.save()
        is_record_updated = True
    except Exception as e:
        is_record_updated = False
    return is_record_updated

def insert_json_data_in_final_json(req_id):
    global final_json
    final_json = {}
    CONNECTION_STRING = read_data_from_blob_cron.CONNECTION_STRING
    CONTAINER_NAME = read_data_from_blob_cron.CONTAINER_NAME
    source_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    source_container_client = source_client.get_container_client(container=CONTAINER_NAME)

    for blob in source_container_client.list_blobs(name_starts_with="Ubona_StagingData"):
        if blob.name.lower().startswith("ubona_stagingdata"):  # and blob.name.lower().endswith(".mp3"):
            if blob.name.lower().endswith(".json") and req_id in blob.name: #) and (req_id in blob.name.lower().split(".")):
                final_json = read_data_from_blob_cron.read_json_properties(source_container_client, blob.name)

def customer_agent_sentiment_in_final_json(count_dic):
    global final_json
    final_json["metadata"]["sentiment_score"]["total_customer_positive_statements"] = count_dic["Customer"]["POSITIVE"]
    final_json["metadata"]["sentiment_score"]["total_customer_negative_statements"] = count_dic["Customer"]["NEGATIVE"]
    final_json["metadata"]["sentiment_score"]["total_customer_neutral_statements"] = count_dic["Customer"]["NEUTRAL"]
    final_json["metadata"]["sentiment_score"]["total_agent_positive_statements"] = count_dic["Agent"]["POSITIVE"]
    final_json["metadata"]["sentiment_score"]["total_agent_negative_statements"] = count_dic["Agent"]["NEGATIVE"]
    final_json["metadata"]["sentiment_score"]["total_agent_neutral_statements"] = count_dic["Agent"]["NEUTRAL"]


def transcribe(audio_uri, locale, request_id):
    global final_json
    update_status(request_id, "In Progress")

    json_filename_with_full_path = BASE_DIR.replace("\\", "/") + "/media/" + request_id + ".json"
    txt_filename_with_full_path = BASE_DIR.replace("\\", "/") + "/media/" + request_id + ".txt"

    is_succeeded = True

    logging.info("Starting transcription client...")

    # configure API key authorization: subscription_key
    configuration = cris_client.Configuration()
    configuration.api_key["Ocp-Apim-Subscription-Key"] = SUBSCRIPTION_KEY
    configuration.host =  f"https://{SERVICE_REGION}.api.cognitive.microsoft.com/speechtotext/v3.0"

    # create the client object and authenticate
    client = cris_client.ApiClient(configuration)

    # create an instance of the transcription api class
    api = cris_client.DefaultApi(api_client=client)

    # Specify transcription properties by passing a dict to the properties parameter. See
    # https://docs.microsoft.com/azure/cognitive-services/speech-service/batch-transcription#configuration-properties
    # for supported parameters.

    delete_all_transcriptions(api)

    properties = {
        "punctuationMode": "DictatedAndAutomatic",
        # "profanityFilterMode": "Masked",
        "wordLevelTimestampsEnabled": True,
        "diarizationEnabled": True,
        "diarizationMinSpeakers": 1,
        "diarizationMaxSpeakers": 2
        # "destinationContainerUrl": "<results container>",
        # "timeToLive": "PT1H"
    }

    # Use base models for transcription. Comment this block if you are using a custom model.
    transcription_definition = transcribe_from_single_blob(audio_uri, properties, locale)

    # Uncomment this block to use custom models for transcription.
    # transcription_definition = transcribe_with_custom_model(api, audio_uri, properties)

    # Uncomment this block to transcribe all files from a container.
    # transcription_definition = transcribe_from_container(RECORDINGS_CONTAINER_URI, properties)

    created_transcription, status, headers = api.create_transcription_with_http_info(
        transcription=transcription_definition)

    # get the transcription Id from the location URI
    transcription_id = headers["location"].split("/")[-1]

    # Log information about the created transcription. If you should ask for support, please
    # include this information.
    logging.info(f"Created new transcription with id '{transcription_id}' in region {SERVICE_REGION}")

    logging.info("Checking status.")

    completed = False

    while not completed:
        # wait for 5 seconds before refreshing the transcription status
        time.sleep(5)

        transcription = api.get_transcription(transcription_id)
        logging.info(f"Transcriptions status: {transcription.status}")

        if transcription.status in ("Failed", "Succeeded"):
            completed = True

        if transcription.status == "Succeeded":
            is_succeeded = True
            pag_files = api.get_transcription_files(transcription_id)
            for file_data in _paginate(api, pag_files):
                if file_data.kind != "Transcription":
                    continue

                audiofilename = file_data.name
                results_url = file_data.links.content_url
                results = requests.get(results_url)

                with open(json_filename_with_full_path, "w+",
                          encoding="utf-8") as file:
                    file.write(results.content.decode("utf-8"))
        elif transcription.status == "Failed":
            is_succeeded = False
            logging.error(f"Transcription failed: {transcription.properties.error.message}")
            with open(json_filename_with_full_path, "w+",
                      encoding="utf-8") as file:
                file.write(transcription.properties.error.message)

    if is_succeeded:
        update_status(request_id, "Completed")
        is_extracted = get_conversation(json_filename_with_full_path, txt_filename_with_full_path)
        insert_json_data_in_final_json(request_id)
        if is_extracted:
            blob_data = Analytic.objects.get(request_id=request_id)
            blob_data.transcribed_file = request_id + ".txt"
            blob_data.save()
            if blob_data.call_language.lower() == "english" or blob_data.call_language.lower() == "hindi":
                language = "en" if blob_data.call_language.lower() == "english" else "hi"
                inferencing(json_filename_with_full_path, txt_filename_with_full_path, language)
                count_dic = count(json_filename_with_full_path, txt_filename_with_full_path, language)
                with open(txt_filename_with_full_path.split(".")[0] + "_" + "count.txt", "r", encoding="utf8") as file:
                    result = file.readlines()
                    overall_count = "".join(result)
                with open(txt_filename_with_full_path.split(".")[0] + "_" + "customer.txt", "r",
                          encoding="utf8") as file:
                    result = file.readlines()
                    customer_agent = "".join(result)                  
                #Finding and storing customer="S1" or "S2" from _customer.txt file
                for x in result:
                    if "customer" in x:
                        customer = x.split("=")[-1].strip()

                name = open(json_filename_with_full_path.split(".")[0] + "_" + "interfencing.json", "r",
                            encoding="utf8")
                data = json.load(name)
                sentiment_results = data.get("sentiment_results", False)
                if sentiment_results:
                    with open(txt_filename_with_full_path, "w+") as file:
                        customer_sentiment_count = []
                        agent_sentiment_count = []
                        #Replaceing S1 with respective customer or agent and writing in text file
                        for row in data["sentiment_results"]:
                            if(row['Speaker'] == customer):
                                speaker = "Customer"
                                customer_sentiment_count.append(row["Prediction"])
                            else:
                                speaker = "Agent"
                                agent_sentiment_count.append(row["Prediction"])
                                
                            line = "{0} : {1} ===== {2} \n".format(speaker, row["Text"], row["Prediction"])
                            file.write(line)
                    if language == "en":
                        qa = qa_main(txt_filename_with_full_path)
                        with open(txt_filename_with_full_path.split(".")[0] + "_" + "qa.txt", "r", encoding="utf8") as file:
                                result = file.readlines()
                                overall_qa = "".join(result)
                    else:
                        qa = qa_main_hindi(txt_filename_with_full_path)
                        with open(txt_filename_with_full_path.split(".")[0] + "_" + "qa.txt", "r", encoding="utf8") as file:
                                result = file.readlines()
                                overall_qa = "".join(result)
                    final_json["metadata"]["sentiment_score"] = {}
                    with open(txt_filename_with_full_path, "a+") as file:
                        file.write("\n=========================\n")
                        file.write(f"Total Number of Statements: {len(agent_sentiment_count+customer_sentiment_count)}\
                                     \nTotal Number Customer Statements: {len(customer_sentiment_count)}\
                                     \nTotal Number Agent Statements: {len(agent_sentiment_count)}\n")
                        final_json["metadata"]["sentiment_score"]["total_number_of_statements"] = len(agent_sentiment_count+customer_sentiment_count)
                        final_json["metadata"]["sentiment_score"]["total_number_of_customer_statements"] = len(customer_sentiment_count)
                        final_json["metadata"]["sentiment_score"]["total_number_of_agent_statements"] = len(agent_sentiment_count)
                        file.write("\n=========================\n")
                        file.write("\n" + overall_count + "\n")
                        customer_agent_sentiment_in_final_json(count_dic)
                        customer_last_positive = customer_sentiment_count[-3:].count("POSITIVE")
                        customer_last_neutral = customer_sentiment_count[-3:].count("NEUTRAL")
                        customer_last_negative = customer_sentiment_count[-3:].count("NEGATIVE")
                        file.write(f"Customer Last 3 Statments:-\n \
                            \nTotal Number of Positive Statements: {customer_last_positive} \
                            \nTotal Number of Neutral Statements: {customer_last_neutral} \
                            \nTotal Number of Negative Statements: {customer_last_negative}\n")
                        final_json["metadata"]["sentiment_score"]["last_three_customer_positive_statements"] = customer_last_positive
                        final_json["metadata"]["sentiment_score"]["last_three_customer_neutral_statements"] = customer_last_neutral
                        final_json["metadata"]["sentiment_score"]["last_three_customer_negative_statements"] = customer_last_negative
                        file.write("\n=========================\n")
                        a = customer_sentiment_count.count("POSITIVE")
                        c = customer_sentiment_count.count("NEGATIVE")
                        d=  customer_last_positive
                        e = customer_last_negative
                        try:
                            n = (a - d) - (c - e)
                            d = a + c
                            dy = n / d
                            x = dy * 0.8

                            if d == 0 and e == 0:
                                y = 0
                            else:
                                y = (((d - e) / d + e) * 0.2)

                            final_sentiment_percent = (x + y) * 100







                        except ZeroDivisionError:
                            file.write(f"\nTotal Sentiment % => Not Defined(Division by 0)\n")
                            final_json["metadata"]["sentiment_score"]["final_sentiment_percent"] = "Not Defined(Division by 0)"
                        else:
                            file.write(f"\nTotal Sentiment % => {round(final_sentiment_percent,2)}%\n")
                            final_json["metadata"]["sentiment_score"]["final_sentiment_percent"] = round(final_sentiment_percent,2)
                        file.write("\n=========================\n")
                        final_json["metadata"]["quality_score"] = {}
                        if language == "en":
                            final_json["metadata"]["quality_score"]["final_score"] = qa["final_score"]
                            final_json["metadata"]["quality_score"]["score_details"] = qa["score_details"]
                            final_json["metadata"]["escalation_for_manager"] = True if qa["fl_escalation_found"] == 1 else False
                            final_json["metadata"]["transcribed_status"] = "Completed"
                        else:
                            final_json["metadata"]["quality_score"]["final_score"] = qa["final_score"]
                            final_json["metadata"]["quality_score"]["score_details"] = qa["score_details"]
                            final_json["metadata"]["escalation_for_manager"] = qa["fl_escalation_found"]
                            final_json["metadata"]["transcribed_status"] = "Completed"
                        file.write(overall_qa+"\n")
                        file.write("\n=========================\n")
                        file.write("\n"+customer_agent)
                    
                    blob_data = Analytic.objects.get(request_id=request_id)
                    blob_data.qa_score = qa['final_score']
                    blob_data.qa_color = qa['final_colour']
                    blob_data.qa_escalation = qa['fl_escalation_found']
                    try:
                        blob_data.sentiment_score = round(final_sentiment_percent,2)
                    except Exception:
                        blob_data.sentiment_score = "INF"
                    blob_data.save()
                    final_json_filename_fullpath = txt_filename_with_full_path.split(".")[0] + "_" + "final.json"
                    with open(final_json_filename_fullpath,"w") as json_outfile:
                        json.dump(final_json, json_outfile, indent = 2)
                    upload_file = request_id+"_final.json"
                    upload_file_to_azure(final_json_filename_fullpath, upload_file)
                    upload_file = request_id+".txt"
                    upload_file_to_azure(txt_filename_with_full_path, upload_file)
                    
    else:
        update_status(request_id, "Failed")

    return True


def main_transcription(req_id):
    try:
        blob_data = Analytic.objects.get(request_id=req_id)
        blob_data.transcribed_file = req_id + ".json"
        blob_data.transcription_start_date_time = timezone.now()
        blob_data.save()
        mp3_blob_name = blob_data.mp3_blob_path
        language = LANGUAGE.get(blob_data.call_language.lower(), False)
        if not language:
            update_status(req_id, "Failed")
            txt_filename_with_full_path = BASE_DIR.replace("\\", "/") + "/media/" + req_id + ".txt"
            with open(txt_filename_with_full_path, "w", encoding="utf-8") as text_file:
                text_file.write("Failed due to unsupported language.")
            return None
        else:
            mp3_uri = get_public_url_of_blob(mp3_blob_name)
            transcribe(mp3_uri, language, req_id)
            blob_data = Analytic.objects.get(request_id=req_id)
            blob_data.transcription_complete_date_time = timezone.now()
            blob_data.save()
            return None
    except Exception as e:
        logging.error("Transcription failed: Reuqest ID: {0} Error: {1}".format(req_id, traceback.format_exc()))

def process_file_for_transcription():
    get_total_count = CurrentProcessLog.objects.all().count()
    if get_total_count == 0:
        obj = CurrentProcessLog(process_status="Stopped")
        obj.save()
    obj = CurrentProcessLog.objects.first()
    running_status = obj.process_status
    if running_status == "Stopped":
        obj.process_status = "Running"
        obj.save()
        proc = []
        in_process = []
        not_started = list(Analytic.objects.filter(transcription_status='Not Started'))[::-1]
        while((len(in_process) <= 15) and (not_started != [])):
            in_process.append(not_started.pop(0))
        for process in in_process:
            p = Process(target=main_transcription, args=(process.request_id,))
            p.start()
            proc.append(p)
        for p in proc:
            p.join()
        obj.process_status = "Stopped"
        obj.save()
        
    



# def process_file_for_transcription():
#     get_total_count = CurrentProcessLog.objects.all().count()
#     if get_total_count == 0:
#         Obj = CurrentProcessLog()
#         Obj.process_id = 1
#         Obj.save()
#         get_request_id = Analytic.objects.get(id=1)
#         req_id = get_request_id.request_id
#         main_transcription(req_id)
#         # path = BASE_DIR.replace("\\", "/") + "/" + "SpeechText/"
#         # file_path_with_argument = "python {0}TranscribeService.py {1}".format(path, req_id)
#         # os.system(file_path_with_argument)
#         # subprocess.Popen(file_path_with_argument, shell=False)
#     else:
#         last_id = CurrentProcessLog.objects.latest('id')
#         check_transcription_status = Analytic.objects.get(id=last_id.process_id)
#         if check_transcription_status.transcription_status == "Failed" or check_transcription_status.transcription_status == "Completed":
#             try:
#                 Analytic.objects.get(id=int(last_id.process_id) + 1)
#                 is_next_id_present = True
#             except Exception as e:
#                 is_next_id_present = False
#             if is_next_id_present:
#                 increase_id = int(last_id.process_id) + 1
#                 last_id.process_id = increase_id
#                 last_id.save()
#                 if check_transcription_status.id == int(last_id.process_id):
#                     fine_nxt_req_id = Analytic.objects.get(id=last_id.process_id + 1)
#                     req_id = fine_nxt_req_id.request_id
#                     main_transcription(req_id)
#                     # path = BASE_DIR.replace("\\", "/") + "/" + "SpeechText/"
#                     # file_path_with_argument = "python {0}TranscribeService.py {1}".format(path, req_id)
#                     # os.system(file_path_with_argument)
#                     # subprocess.Popen(file_path_with_argument, shell=False)
#         elif check_transcription_status.transcription_status == "In Progress":
#             return None
#         elif check_transcription_status.transcription_status == "Not Started":
#             last_id = CurrentProcessLog.objects.latest('id')
#             check_transcription_status = Analytic.objects.get(id=last_id.process_id)
#             req_id = check_transcription_status.request_id
#             main_transcription(req_id)
#             # print(req_id)
#             # path = BASE_DIR.replace("\\", "/") + "/" + "SpeechText/"
#             # file_path_with_argument = "python {0}TranscribeService.py {1}".format(path, req_id)
#             # os.system(file_path_with_argument)
#             # subprocess.Popen(file_path_with_argument, shell=False)