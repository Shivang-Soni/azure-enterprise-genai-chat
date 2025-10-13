from azure.ai.openai import OpenAIClient
from azure.identity import DefaultAzureCredential
from app.config import AZURE_OPEN_AI_ENDPOINT, AZURE_OPENAI_KEY
import os

class OpenAIClientWrapper:
    def __init__(self):
        self.client = OpenAIClient(
            endpoint=AZURE_OPEN_AI_ENDPOINT,
            credential=AZURE_OPENAI_KEY
        )
    
    def generate_answer(self, prompt: str, model: str = "gpt-35-turbo", max_tokens: int = 300 ):
        '''
        Zuständig für die Erzeugung einer Antwort mit Azure OpenAI (GPT).
        '''
        response = self.client.chat_completions.create(
            deployment_name=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content