from azure.ai.openai import OpenAIClient
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from app.config import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY
import os

class OpenAIClientWrapper:
    def __init__(self):
        self.client = OpenAIClient(
            endpoint=AZURE_OPENAI_ENDPOINT,
            credential=AzureKeyCredential(AZURE_OPENAI_KEY)
        )
    
    def generate_answer(self, prompt: str, model: str = "gpt-35-turbo", max_tokens: int = 300 ):
        """
        Zuständig für die Erzeugung einer Antwort mit Azure OpenAI (GPT).
        """
        response = self.client.chat_completions.create(
            deployment_name=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content