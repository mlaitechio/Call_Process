import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

CLOUD_PATH = "DefaultEndpointsProtocol=https;AccountName=storagemlai123;AccountKey=5BF4Kw9C6j//ynGQronaU8MMD2hNSw+DjztWxLN3+D0yGYJK+AdhZdFCdJJJPHTX/xEStSwhepc/nRlTvSGWcQ==;EndpointSuffix=core.windows.net"


def upload_file_to_azure_storage(file_name, file_path):
    AZURE_STORAGE_CONNECTION_STRING = CLOUD_PATH
    CONTAINER_NAME = 'abtest-' + str(uuid.uuid4())
    data = {}
    try:
        # connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        connect_str = AZURE_STORAGE_CONNECTION_STRING
        # print(connect_str)

        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # Create a unique name for the container
        container_name = CONTAINER_NAME

        # Create the container

        container_client = blob_service_client.create_container(container_name)

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

        # print("\nUploading to Azure Storage as blob:\n\t" + upload_file_path)

        # Upload the created file
        with open(file_path + "/" + file_name, "rb") as sfile:
            blob_client.upload_blob(sfile)

        # print("\nListing blobs...")
        #
        # # List the blobs in the container
        # blob_list = container_client.list_blobs()
        # for blob in blob_list:
        #     print("\t" + blob.name)

        # print("Deleting blob container...")
        # container_client.delete_container()

        # print(blob_service_client.account_name)
        # print(blob_service_client.credential.account_key)

        # sas_token = generate_account_sas(
        #     account_name=blob_service_client.account_name,
        #     account_key=blob_service_client.credential.account_key,
        #     resource_types=ResourceTypes(service=True),
        #     permission=AccountSasPermissions(read=True, write=True),
        #     expiry=datetime.utcnow() + timedelta(hours=1)
        # )

        sas_token = generate_blob_sas(
            account_name=blob_service_client.account_name,
            account_key=blob_service_client.credential.account_key,
            container_name=CONTAINER_NAME,
            blob_name=file_name,
            permission=BlobSasPermissions(read=True, write=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )
        url = "https://" + blob_service_client.account_name + ".blob.core.windows.net/" + CONTAINER_NAME + "/" + file_name + "?" + sas_token
        data["url"] = url
    except Exception as e:
        print('Error: Unable to Upload File to Blob')
        data["exception"] = e
    # print("=" * 20 + "BLOB URI" + "=" * 20)
    # print(data)
    # print("=" * 20 + "BLOB URI" + "=" * 20)
    return data
