from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import AccountSasPermissions
import json

ACCOUNT_NAME = "abaccallcenteranalysisdi"
ACCOUNT_KEY = "pM2O2eoz3Xut7XjYs5QzvD3t6RtGmLYsoW2bLfx8BSMe0T9KUeayHFlqyb2tojHv2+ah4+U5tQcdFOqXbCARdA=="
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=abaccallcenteranalysisdi;AccountKey=pM2O2eoz3Xut7XjYs5QzvD3t6RtGmLYsoW2bLfx8BSMe0T9KUeayHFlqyb2tojHv2+ah4+U5tQcdFOqXbCARdA==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "ubonadata-storage"


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
