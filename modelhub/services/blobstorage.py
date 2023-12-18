import os
from datetime import date

import dotenv
from azure.storage.blob import BlobServiceClient

dotenv.load_dotenv()


class BlobStorageAccessPoint:
    """
    Access point to the blob storage.
    """

    def __init__(self):
        access_token = os.environ.get("MODELHUB_STORAGE_ACCESS_TOKEN")
        self.blob_service_client = BlobServiceClient.from_connection_string(
            access_token,
        )

    def upload_blob(self, path):
        """
        Upload model to the blob storage.
        """

        # If there are more than 5 models in the blob storage, remove the oldest ones
        self.remove_oldest_models()

        blob_name = os.path.basename(path)
        blob_client = self.blob_service_client.get_blob_client(
            container="model-logs",
            blob=blob_name,
        )
        try:
            with open(file=path, mode="rb") as data:
                blob_client.upload_blob(data, overwrite=False)
            print(f"Uploaded {blob_name} successfully!")
        except Exception as e:
            print(f"Error uploading {blob_name}: {e}")

    def pull_models(self):
        """
        Pull models from the blob storage, daily.
        """
        download_folder = os.path.join(os.getcwd(), "models")
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        container_client = self.blob_service_client.get_container_client("model-logs")
        today = date.today()
        blobs = container_client.list_blobs()
        for blob in blobs:
            # Only download the models from today
            if today.strftime("%Y-%m-%d") not in blob.name:
                return
            blob_name = blob.name
            download_path = os.path.join(download_folder, blob_name)
            blob_client = self.blob_service_client.get_blob_client(
                container="model-logs",
                blob=blob_name,
            )
            with open(download_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())

    def remove_oldest_models(self):
        """
        Remove the oldest models from the blob storage.
        """
        container_client = self.blob_service_client.get_container_client("model-logs")
        blobs = container_client.list_blobs()
        blob_list = []
        for blob in blobs:
            blob_list.append(blob)
        if len(blob_list) <= 5:
            return
        blob_list.sort(key=lambda x: x.last_modified)
        for blob in blob_list[:-3]:
            container_client.delete_blob(blob.name)
            print(f"Deleted {blob.name} successfully!")
