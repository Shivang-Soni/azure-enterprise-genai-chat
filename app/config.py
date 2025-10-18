# app/config.py
import os
import logging

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Logger Konfiguration
logger = logging.getLogger("config")

# .env wird geladen
load_dotenv()

# Key Vault Client Einrichtung
AZURE_KEY_VAULT_URL = os.getenv("AZURE_KEY_VAULT_URL", "")

if AZURE_KEY_VAULT_URL:
    try: 
        credential = DefaultAzureCredential()
        secret_client = SecretClient(AZURE_KEY_VAULT_URL, credential=credential)
    except Exception as e:
        logger.warning(f"Key Vault konnte nicht initialisiert werden: {e}")
        secret_client = None
else:
    secret_client = None

def get_secret(name: str, fallback: str = "") -> str:
    """
    Versucht es, das genannte Geheimnis aus dem Vault zu holen.
    Falls es nicht vorhanden oder zugänglich ist,
    wird der in der .env vorhandenen Wert eingesetzt.
    """
    if secret_client:
        try:
            keyvault_name = name.lower().replace("_", "-")
            return secret_client.get_secret(keyvault_name).value
        except Exception:
            logger.warning(
                f"Das Geheimnis: {name} konnte in Key Vault nicht gefunden werden."
                "Somit wird es aus der .env Datei geladen."
            )
    return os.getenv(name, fallback)

# Azure Konfiguration
AZURE_SEARCH_ENDPOINT = get_secret("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = get_secret("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = get_secret("AZURE_SEARCH_INDEX")

AZURE_OPENAI_ENDPOINT = get_secret("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = get_secret("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = get_secret("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_VERSION = get_secret("AZURE_OPENAI_VERSION")

AZURE_BLOB_CONTAINER = get_secret("AZURE_BLOB_CONTAINER")
AZURE_BLOB_SAS_TOKEN = get_secret("AZURE_BLOB_SAS_TOKEN")
AZURE_BLOB_ACCOUNT = get_secret("AZURE_BLOB_ACCOUNT")
