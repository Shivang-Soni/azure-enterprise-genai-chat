import logging
from typing import List

import json

from azure.storage.blob import ContainerClient

from app.config import AZURE_BLOB_CONN_STR, AZURE_BLOB_CONTAINER

# Initialiserung vom Logger
logger = logging.getLogger(__name__)


class BlobStorageClient:
    """
    Verwaltet Uploads, Downloads, und Auflistungen 
    von Dateien in Azure Blob Storage.
    """

    def __init__(self):
        """
        Initialisiert die Verbindung zu Azure Blob Storage
        """
        try:
            # ContainerClient wird unmittelbar mit SAS URL erstellt.
            self.container_client = ContainerClient.from_container_url(
                container_url=f"{AZURE_BLOB_CONN_STR}"
            )
            logger.info(
                "Azure Blob Storage Client wurde erfolgreich initialisiert"
                )
        except Exception as e:
            logger.error(
                f"Fehler bei der Initialisierung von BlobStorageClient: {e}"
                )
            raise

    def upload_file(self, data: dict) -> bool:
        """
        Lädt eine lokale Datei in den Blob Speicher hoch.
        """
        try:
            blob_client = self.container_client.get_blob_client(
                AZURE_BLOB_CONTAINER
                )
            blob_client.upload_blob(json.dumps(data, ensure_ascii=False), overwrite=True)
            logger.info(f"Datei: {AZURE_BLOB_CONTAINER} erfolgreich geladen.")
            return True
        except Exception as e:
            logger.error(
                f"Fehler beim Hochladen der Datei {AZURE_BLOB_CONTAINER}: {e}"
                )
            return False

    def download_file(self, blob_name: str, download_path: str) -> bytes:
        """
        Lädt eine Datei aus dem Blob-Container herunter.
        """
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            data = blob_client.download_blob().readall()
            logger.info(f"Datei: {blob_name} erfolgreich heruntergeladen.")
            return data
        except Exception as e:
            logger.error(f"Fehler beim Herunterladen von '{blob_name}': {e}")
            return None

    def list_files(self):
        """
        Gibt eine Liste aller Dateien im Container zurück.
        """
        try:
            return [blob.name for blob in self.container_client.list_blobs()]
        except Exception as e:
            logger.error(f"Fehler beim Auflisten von Dateien: {e}")
            return []
