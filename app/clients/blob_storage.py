from azure.storage.blob import BlobServiceClient
import os
from app.config import AZURE_BLOB_CONN_STR, AZURE_BLOB_CONTAINER

class BlobStorageClient:
    def __init__(self):
        '''
        Initialisiert die Verbindung zu Azure Blob Storage
        '''
        self.blob_service_client = BlobServiceClient.from_connection_string(
            AZURE_BLOB_CONN_STR
        )
        self.container_client = self.blob_service_client.get_container_client(
            AZURE_BLOB_CONTAINER
        )

    def upload_file(self, file_path: str, blob_name: str):
        '''
        Lädt eine lokale Datei in den Blob Speicher hoch.
        '''
        with open(file_path, "rb") as data:
            self.container_client.upload_blob(
                name=blob_name,
                data=data,
                overwrite=True)
        return f"Datei: {blob_name} erfolgreich geladen."
    
    def download_file(self, blob_name: str, download_path: str):
        '''
        Lädt eine Datei vom Blob Speicher herunter.
        '''
        blob_client = self.container_client.get_blob_client(blob_name)
        with open(download_path, "wb") as file:
            file.write(blob_client.download_blob().readall())
        return f"Datei '{blob_name}' wurde erfolgreich geladen."
    
    def list_files(self):
        '''
        Listet alle Blobs im Container auf.
        '''
        return [blob.name for blob in self.container_client.list_blobs()]