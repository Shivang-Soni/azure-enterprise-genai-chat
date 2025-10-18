import logging

from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.search.documents import SearchClient

from app.config import  \
    AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_INDEX, AZURE_SEARCH_KEY

# Initialisierung von Logger
logger = logging.getLogger(__name__)


class CoginitiveSearchClient:
    def __init__(self):
        try:
            # Zur Erhöhung der Robustheit:
#  Überprüfung davon, ob alle bereits vorhanden sind
            if not all([AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_INDEX, AZURE_SEARCH_KEY]):
                raise ValueError("Azure Cognitive Search Konfigurationswerte fehlen!")
            self.client = SearchClient(
                endpoint=AZURE_SEARCH_ENDPOINT,
                index_name=AZURE_SEARCH_INDEX,
                credential=AzureKeyCredential(AZURE_SEARCH_KEY),
                )
        except Exception as e:
            logger.info(
                f"Fehler bei der Initialisierung von CognitiveSearchClient: {e}"
                )
            raise

    def search_documents(self, query: str, top: int = 5):
        """
        Führt eine Suche in Azure Cognitive Search durch.
        Gibt die Top-Dokumente als Liste von Dictionaries zurück.
        """
        try:
            results = self.client.search(
                search_text=query, 
                top=top
                )
            return [doc for doc in results]
        except HttpResponseError as e:
            logger.error(f"Fehler bei der Suchanfrage: {e}")
            return []
