import logging
from fastapi import FastAPI
from app.clients.keyvault import AzureKeyVaultClient

app = FastAPI(title="Azure Enterprise GenAI Chat")

@app.on_event("startup")
async def startup_event():
    key_vault_client = AzureKeyVaultClient
    openai_key = key_vault_client.get_secret("OPENAI_API_KEY")
    if openai_key:
        logging.info("Geheimnis wurde erfolgreich aus dem Key Vault geladen")
    else:
        logging.error("Geheimnis konnte nicht geladen werden")

@app.get("/")
def health():
    return {"status": "OK"}
