from azure.storage.blob import BlobServiceClient
import logging
#from ABC.settings import BASE_DIR
import os
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACCOUNT_NAME = "abaccallcenteranalysisdi"
ACCOUNT_KEY = "pM2O2eoz3Xut7XjYs5QzvD3t6RtGmLYsoW2bLfx8BSMe0T9KUeayHFlqyb2tojHv2+ah4+U5tQcdFOqXbCARdA=="
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=abaccallcenteranalysisdi;AccountKey=pM2O2eoz3Xut7XjYs5QzvD3t6RtGmLYsoW2bLfx8BSMe0T9KUeayHFlqyb2tojHv2+ah4+U5tQcdFOqXbCARdA==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "ubonadata-storage"

source_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
source_container_client = source_client.get_container_client(container=CONTAINER_NAME)

#full_file_path = os.path.join(BASE_DIR, 'media/').replace('\\', '/')

def upload_file_to_azure(final_json_filename_fullpath, upload_file):
    blob_client = source_client.get_blob_client(container=CONTAINER_NAME, blob="transcription_results/"+upload_file)
    print("Uploading "+upload_file + " in container "+CONTAINER_NAME)
    with open(final_json_filename_fullpath,"rb") as file_data:
        blob_client.upload_blob(file_data, overwrite=True)

# for file_name in os.listdir(full_file_path):
#     if file_name.split(".")[-1] != "zip":
#         blob_client = source_client.get_blob_client(container=CONTAINER_NAME, blob="transcription_results/"+file_name)

#         print("Uploading "+file_name+" in container "+CONTAINER_NAME)

#         with open(full_file_path+file_name,"rb") as file_data:
#             blob_client.upload_blob(file_data, overwrite=True)

#         url = "https://" + source_client.account_name + ".blob.core.windows.net/" + CONTAINER_NAME + "/transcription_results/" + file_name
#         print(url)
