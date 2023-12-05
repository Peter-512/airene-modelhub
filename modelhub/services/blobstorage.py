import os

import dotenv
from azure.storage.blob import BlobServiceClient

dotenv.load_dotenv()


class BlobStorageAccessPoint:
    def __init__(self):
        account_url = os.environ["MODELHUB_BLOB_ACCOUNT_URL"]
        sas = os.environ["MODELHUB_BLOB_SAS_TOKEN"]
        self.blob_service_client = BlobServiceClient(account_url, credential=sas)

    def upload_blob(self, path):
        blob_client = self.blob_service_client.get_blob_client(
            container="model-logs",
            blob=path.split("/")[-1],
        )
        try:
            with open(file=path, mode="rb") as data:
                blob_client.upload_blob(data)
            print("Uploaded succesfully!")
        except Exception:
            print(f"Blob already exists for {path}")
