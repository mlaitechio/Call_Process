import logging
import requests
import time
import swagger_client as cris_client

import sys
import os
import django
import traceback

from django.utils import timezone

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")

sys.path.append("/".join(os.getcwd().replace("\\", "/").split("/")[0:-1]))
os.environ['DJANGO_SETTINGS_MODULE'] = 'ABC.settings'
django.setup()

from AbcApp.models import Analytic
#from ABC.settings import BASE_DIR
BASE_DIR='/home/data'

from SpeechText.ExtractConversation import get_conversation
from SpeechText.GetPublicUrlBlob import get_public_url_of_blob

LANGUAGE = {"english": "en-IN", "hindi": "hi-IN"}
SUBSCRIPTION_KEY = "8a8ab9aea0ce4d06b318a8983d3d2adb"
SERVICE_REGION = "centralindia"

NAME = "Simple transcription"
DESCRIPTION = "Simple transcription description"

# Set subscription information when doing transcription with custom models
ADAPTED_ACOUSTIC_ID = None  # guid of a custom acoustic model
ADAPTED_LANGUAGE_ID = None  # guid of a custom language model


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


def transcribe(audio_uri, locale, request_id):
    update_status(request_id, "In Progress")

    json_filename_with_full_path = BASE_DIR.replace("\\", "/") + "/media/" + request_id + ".json"
    txt_filename_with_full_path = BASE_DIR.replace("\\", "/") + "/media/" + request_id + ".txt"

    is_succeeded = True

    logging.info("Starting transcription client...")

    # configure API key authorization: subscription_key
    configuration = cris_client.Configuration()
    configuration.api_key["Ocp-Apim-Subscription-Key"] = SUBSCRIPTION_KEY
    configuration.host = f"https://{SERVICE_REGION}.api.cognitive.microsoft.com/speechtotext/v3.0"

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
        "diarizationEnabled": True
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
        if is_extracted:
            blob_data = Analytic.objects.get(request_id=request_id)
            blob_data.transcribed_file = request_id + ".txt"
            blob_data.save()
    else:
        update_status(request_id, "Failed")

    return True


def main(req_id):
    try:
        blob_data = Analytic.objects.get(request_id=req_id)
        blob_data.transcribed_file = req_id + ".json"
        blob_data.transcription_start_date_time = timezone.now()
        blob_data.save()
        mp3_blob_name = blob_data.mp3_blob_path
        language = LANGUAGE[blob_data.call_language.lower()]
        mp3_uri = get_public_url_of_blob(mp3_blob_name)
        transcribe(mp3_uri, language, req_id)
        blob_data = Analytic.objects.get(request_id=req_id)
        blob_data.transcription_complete_date_time = timezone.now()
        blob_data.save()
    except Exception as e:
        logging.error("Transcription failed: Reuqest ID: {0} Error: {1}".format(req_id, traceback.format_exc()))
