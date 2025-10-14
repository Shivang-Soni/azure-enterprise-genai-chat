import logging

from fastapi import FastAPI
from pydantic import BaseModel

from app.clients.keyvault import AzureKeyVaultClient
from app.services.chat_service import ChatService

app = FastAPI(title="Azure Enterprise GenAI Chat")

# Key Vault und Chat Service
key_vault_client = AzureKeyVaultClient()
chat_service = ChatService()


class ChatRequest(BaseModel):
    user_id: str
    question: str


class ChatResponse(BaseModel):
    answer: str


@app.on_event("startup")
async def startup_event():
    openai_key = key_vault_client.get_secret("OPENAI_API_KEY")
    if openai_key:
        logging.info("Geheimnis wurde erfolgreich aus dem Key Vault geladen")
    else:
        logging.error("Geheimnis konnte nicht geladen werden")


@app.get("/")
def health():
    return {"status": "OK"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    answer = chat_service.process_query(request.question, request.user_id)
    return ChatResponse(answer=answer)
