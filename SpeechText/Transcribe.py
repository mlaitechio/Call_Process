import logging
import os
import sys
import requests
import time
import swagger_client as cris_client

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")

SUBSCRIPTION_KEY = "8a8ab9aea0ce4d06b318a8983d3d2adb"
SERVICE_REGION = "centralindia"

NAME = "Simple transcription"
DESCRIPTION = "Simple transcription description"
LOCALE = "hi-IN"

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


def transcribe_from_single_blob(uri, properties):
    """
    Transcribe a single audio file located at `uri` using the settings specified in `properties`
    using the base model for the specified locale.
    """
    transcription_definition = cris_client.Transcription(
        display_name=NAME,
        description=DESCRIPTION,
        locale=LOCALE,
        content_urls=[uri],
        properties=properties
    )

    return transcription_definition


def transcribe(audio_uri, json_filename_with_full_path):
    is_succeeded = True

    logging.info("Starting transcription client...")

    # if os.path.exists(str(os.path.dirname(os.path.abspath(__file__))) + "/result.json"):
    #     os.remove(str(os.path.dirname(os.path.abspath(__file__))) + "/result.json")

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
    transcription_definition = transcribe_from_single_blob(audio_uri, properties)

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

                with open(json_filename_with_full_path, "w",
                          encoding="utf-8") as file:
                    file.write(results.content.decode("utf-8"))
        elif transcription.status == "Failed":
            is_succeeded = False
            logging.info(f"Transcription failed: {transcription.properties.error.message}")
            with open(json_filename_with_full_path, "w",
                      encoding="utf-8") as file:
                file.write(transcription.properties.error.message)

    return is_succeeded


# r = transcribe("https://abaccallcenteranalysisdi.blob.core.windows.net/ubonadata-storage/Ubona_StagingData/2021/05/14/ABML_1620279117704_9954909128_INBOUND_20210506_110157.mp3?se=2021-05-17T18%3A42%3A35Z&sp=r&sv=2019-12-12&sr=b&sig=Kb5J%2BoB8/C0sAqQ4Ozr4fzvKeUZvDx/SLSLg9afm4WM%3D", "r.json")
# print(r)