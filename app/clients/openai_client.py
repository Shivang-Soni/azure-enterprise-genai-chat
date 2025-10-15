import os

from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential

from app.config import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_DEPLOYMENT


class OpenAIClientWrapper:
    def __init__(self):
        self.client = ChatCompletionsClient(
            endpoint=AZURE_OPENAI_ENDPOINT,
            credential=AzureKeyCredential(AZURE_OPENAI_KEY),
        )
        self.deployment = AZURE_OPENAI_DEPLOYMENT

    def generate_answer(
        self, prompt: str, model: str = "gpt-35-turbo", max_tokens: int = 300
    ):
        """
        Zuständig für die Erzeugung einer Antwort mit Azure OpenAI (GPT).
        """
        messages = [
            {"role": "system", "content": "Du bist ein KI-Assistent."},
            {"role": "user", "content": prompt}
        ]

        response = self.client.complete(
           model=self.deployment,
           messages=messages,
           max_tokens=max_tokens
        )
        return response.choices[0].message.content
