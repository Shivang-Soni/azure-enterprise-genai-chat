# ========================================================
# Das Hochladen von meinen Dokumenten
# ========================================================
import json
import logging

from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from app.config import AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_INDEX, AZURE_SEARCH_KEY


# Logger Konfiguration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# KI Suche Initalisierung
search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)
)

# Dokumente aus der JSON Datei importieren
file_name = "docs_info"
with open(f"app/data/{file_name}.json", "r", encoding="utf-8") as f:
    docs = json.load(f)
print(docs)
# Wenn vorhanden, hochladen
if docs:
    result = search_client.upload_documents(documents=docs)
    erfolgreich = True
    for r in result:
        if not r.succeeded:
            logger.warning(f"Dokument wurde nicht hochgeladen: {r.key}.")
            erfolgreich = False

else:
    logger.error("Dokumente konnten nicht gefunden werden.")
    erfolgreich = False

if erfolgreich:
    logger.info("Alle Dateien wurden erfolgreich hochgeladen.")
