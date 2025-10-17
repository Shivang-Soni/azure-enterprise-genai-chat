import sys
import logging
import json
from typing import List, Optional

from azure.storage.blob import ContainerClient

from app.config import AZURE_BLOB_CONN_STR, AZURE_BLOB_CONTAINER

# Initialiserung vom Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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

    def upload_file(self, data: dict, blob_name: str) -> bool:
        """
        Lädt eine lokale Datei in den Blob Speicher hoch.
        """
        if not blob_name:
            logger.warning(
                "Die upload_file Funktion wurde ohne blob_name aufgerufen."
                )
            blob_name = f"chat_{len(self.list_files())}.json"

        try:
            blob_client = self.container_client.get_blob_client(
                blob_name
                )
            payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
            blob_client.upload_blob(payload, overwrite=True)
            logger.info(
                f"Datei: {blob_name} erfolgreich hochgeladen."
                )
            return True
        except Exception as e:
            logger.error(
                f"Fehler beim Hochladen der Datei"
                f"in den Container: {AZURE_BLOB_CONTAINER}: {e}"
                )
            return False

    def download_file(self, blob_name: str) -> Optional[bytes]:
        """
        Lädt eine Datei aus dem Blob-Container herunter
        und gibt deren Bytes zurück.
        Beim Fehler wird None zurückgegeben.
        """
        if not blob_name:
            logger.error(
                "Die download_file Funktion wurde ohne blob_name aufgerufen."
                )

        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            data = blob_client.download_blob().readall()
            logger.info(f"Datei: {blob_name} erfolgreich heruntergeladen.")
            return data
        except Exception as e:
            logger.error(f"Fehler beim Herunterladen von '{blob_name}': {e}")
            return None

    def list_files(self) -> List[str]:
        """
        Gibt eine Liste aller Dateien im Container zurück.
        """
        try:
            return [blob.name for blob in self.container_client.list_blobs()]
        except Exception as e:
            logger.error(f"Fehler beim Auflisten von Dateien: {e}")
            return []
