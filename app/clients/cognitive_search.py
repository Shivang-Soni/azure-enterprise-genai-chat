from azure.core.credentials import AzureKeyCredential 
from azure.search.documents import SearchClient
from app.config import AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_KEY, AZURE_SEARCH_INDEX

class CoginitiveSearchClient:
    def __init__(self):
        self.client = SearchClient(
            endpoint=AZURE_SEARCH_ENDPOINT,
            index=AZURE_SEARCH_INDEX,
            credential=AzureKeyCredential(AZURE_SEARCH_KEY)
        )

    def search_documents(self, query: str, top: int = 5):
        '''
        Führt eine Suche in Azure Cognitive Search durch.
        Gibt die Top-Dokumente zurück.
        '''
        results = self.client.search(search_text=query, top=top)
        return [doc for doc in results]
    
    
