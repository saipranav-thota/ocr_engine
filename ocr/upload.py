import os
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

from urllib.parse import urljoin

# === Load environment variables ===
load_dotenv()


BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")


if not BLOB_CONNECTION_STRING or not BLOB_CONTAINER_NAME:
    raise Exception("Please set BLOB_CONNECTION_STRING and BLOB_CONTAINER_NAME in .env")

# === Setup Azure clients ===
blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)

# === Upload image to Blob Storage ===
def upload_image_to_blob(local_path, blob_name=None, sas_expiry_minutes=60):
    if not blob_name:
        blob_name = os.path.basename(local_path)
    
    blob_client = container_client.get_blob_client(blob_name)
    with open(local_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    account_key = blob_service_client.credential.account_key  # This works only for key-based auth

    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=BLOB_CONTAINER_NAME,
        blob_name=blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=sas_expiry_minutes)
    )

    sas_url = f"{blob_client.url}?{sas_token}"
    return sas_url
    

