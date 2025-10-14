import logging
from typing import List

from azure.storage.blob import BlobServiceClient

from app.config import AZURE_BLOB_CONN_STR, AZURE_BLOB_CONTAINER

# Initialiserung vom Logger
logger = logging.getLogger(__name__)


class BlobStorageClient:
    """
    Verwaltet Uploads, Downloads, und Auflistungen von Dateien in Azure Blob Storage.
    """

    def __init__(self):
        """
        Initialisiert die Verbindung zu Azure Blob Storage
        """
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(
                AZURE_BLOB_CONN_STR
            )
            self.container_client = self.blob_service_client.get_container_client(
                AZURE_BLOB_CONTAINER
            )
            logger.info("Azure Blob Storage Client wurde erfolgreich initialisiert")
        except Exception as e:
            logger.error(f"Fehler bei der Initialisierung von BlobStorageClient: {e}")
            raise

    def upload_file(self, file_path: str, blob_name: str) -> bool:
        """
        Lädt eine lokale Datei in den Blob Speicher hoch.
        """
        try:
            with open(file_path, "rb") as data:
                self.container_client.upload_blob(
                    name=blob_name, data=data, overwrite=True
                )
            logger.info(f"Datei: {blob_name} erfolgreich geladen.")
            return True
        except Exception as e:
            logger.error(f"Fehler beim Hochladen der Datei {blob_name}: {e}")
            return False

    def download_file(self, blob_name: str, download_path: str) -> bool:
        """
        Lädt eine Datei aus dem Blob-Container herunter.
        """
        try:
            with open(download_path, "wb") as file:
                stream = self.container_client.download_blob(blob_name)
                file.write(stream.readall())
            logger.info("Datei: {blob_name} erfolgreich heruntergeladen.")
            return True
        except Exception as e:
            logger.error(f"Fehler beim Herunterladen von '{blob_name}': {e}")
            return False

    def list_files(self):
        """
        Gibt eine Liste aller Dateien im Container zurück.
        """
        try:
            return [blob.name for blob in self.container_client.list_blobs()]
        except Exception as e:
            logger.error("Fehler beim Auflisten von Dateien: {e}")
            return []
