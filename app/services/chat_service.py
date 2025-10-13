import logging
from app.clients.cognitive_search import CoginitiveSearchClient
from app.clients.openai_client import OpenAIClientWrapper
from app.clients.blob_storage import BlobStorageClient
import json

logger = logging.getLogger(__name__)


class ClassService:
    def __init__(self):
        self.search_client = CoginitiveSearchClient()
        self.openai_client = OpenAIClientWrapper()
        self.blob_storage = BlobStorageClient() 

    def process_query(self, question: str, user_id: str):
        """
        1. Suche relevante Dokumente über Cognitive Search
        2. Generiere Antwort über Azure Open AI
        3. Speichere Cloudverlauf in Blob Storage
        """
        # Dokumente aufrufen
        # Prompt für OpenAI vorbereiten 
        # Antwort erzeugen
        # Verlauf speichern
        return answer