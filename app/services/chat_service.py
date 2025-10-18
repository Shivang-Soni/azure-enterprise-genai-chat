import logging

from app.clients.blob_storage import BlobStorageClient
from app.clients.cognitive_search import CoginitiveSearchClient
from app.clients.openai_client import OpenAIClientWrapper

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self):
        self.search_client = CoginitiveSearchClient()
        self.openai_client = OpenAIClientWrapper()
        self.blob_storage = BlobStorageClient()

    def process_query(self, question: str, user_id: str = "default_user"):
        """
        1. Suche relevante Dokumente über Cognitive Search
        2. Generiere Antwort über Azure Open AI
        3. Speichere Cloudverlauf in Blob Storage
        """
        # Dokumente aufrufen
        documents = self.search_client.search_documents(question)
        context_texts = [doc.get("content", "") for doc in documents]
        context_combined = "\n".join(context_texts)

        # Prompt für OpenAI vorbereiten
        prompt = f"""
        Du bist ein KL Assistent.
        Nutze die folgenden Dokumente als Kontext,
        um präzise und professionelle Antworten zu geben,
        ausschließlich aufs Deutsch.
        (Falls keine Dokumente als Kontext vorhanden sind,
        gemäß Ihrem Wissen beantworten.)
        
        Kontext:
        {context_combined}

        Frage:
        {question}
        """

        # Antwort erzeugen
        answer = self.openai_client.generate_answer(prompt)

        # Verlauf speichern
        self._save_conversation(
            user_id,
            {"user_query": question, "answer": answer, "context_used": context_texts},
        )

        # Antwort zurückgeben
        return answer

    def _save_conversation(self, user_id: str, data: dict):
        """
        Speichert das Gespräch im Blob Speicher als JSON Datei.
        """
        self.blob_storage.upload_file(data=data, blob_name=None)
        logger.info(f"Gespräch wurde für {user_id} erfolgreich gespeichert.")
