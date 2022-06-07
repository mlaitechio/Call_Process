from azure.storage.blob import BlobServiceClient
import json

import sys
import os
import django

sys.path.append("/".join(os.getcwd().replace("\\", "/").split("/")[0:-1]))
os.environ['DJANGO_SETTINGS_MODULE'] = 'ABC.settings'
django.setup()

from ABC.settings import BASE_DIR
from AbcApp.models import Analytic, CurrentProcessLog

ACCOUNT_NAME = "absliamcsstoragemlai1"
ACCOUNT_KEY = "RECLddq51PeKWQ8mnsTmCLjtdFEtCoCSDIU0AL9BFt0jydaht/QqpcpT8wDJh//Zi1o7tCsu6XcyMZuIrEyl5g=="
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=absliamcsstoragemlai1;AccountKey=RECLddq51PeKWQ8mnsTmCLjtdFEtCoCSDIU0AL9BFt0jydaht/QqpcpT8wDJh//Zi1o7tCsu6XcyMZuIrEyl5g==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "ubonadata-storage"


def read_json_properties(source_client, blob_name):
    bc = source_client.get_blob_client(
        blob=blob_name)
    data = bc.download_blob()
    read_all = data.readall()
    result = json.loads(read_all.decode('utf-8'))
    return result


def read_data_from_blob():
    source_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    source_container_client = source_client.get_container_client(container=CONTAINER_NAME)
    # print(container_client.account_name, container_client.credential.account_key)
    for blob in source_container_client.list_blobs(name_starts_with="Ubona_StagingData"):
        if blob.name.lower().startswith("ubona_stagingdata"):  # and blob.name.lower().endswith(".mp3"):
            if blob.name.lower().endswith(".json"):
                json_results = read_json_properties(source_container_client, blob.name)
                print(json_results)
                request_id = ""
                call_date = ""
                call_campaign = ""
                call_agent = ""
                call_duration = ""
                call_language = ""
                call_status = ""
                call_json_blob = ""
                call_mp3_blob = ""
                try:
                    blob_name = blob.name
                    request_id = json_results["metadata"]["requestId"]
                    call_date = json_results["metadata"]["date"]
                    call_campaign = json_results["metadata"]["campaign"]
                    call_agent = json_results["metadata"]["agent"]
                    call_duration = json_results["metadata"]["duration"]
                    call_language = json_results["metadata"]["language"]
                    call_status = json_results["metadata"]["callStatus"]
                    call_json_blob = blob_name
                    call_mp3_blob = blob_name.replace(".json", ".mp3")
                    is_data_present = True
                except Exception as e:
                    is_data_present = False
                    print(str(e))

                if is_data_present:
                    # noinspection PyBroadException
                    try:
                        Analytic.objects.get(request_id=request_id)
                    except Exception as e:
                        DB_Object = Analytic()
                        DB_Object.request_id = request_id
                        DB_Object.date_time = call_date
                        DB_Object.campaign = call_campaign
                        DB_Object.agent_name = call_agent
                        DB_Object.call_duration = call_duration
                        DB_Object.call_language = call_language
                        DB_Object.call_status = call_status
                        DB_Object.json_blob_path = call_json_blob
                        DB_Object.mp3_blob_path = call_mp3_blob
                        DB_Object.save()
            elif blob.name.lower().endswith(".mp3"):
                continue
