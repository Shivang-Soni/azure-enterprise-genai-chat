import os

from openai import AzureOpenAI

from app.config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_VERSION
)


class OpenAIClientWrapper:
    def __init__(self):
        """
        Initialisiert den Azure OpenAI Client über das öffentliche OpenAI SDK.
        """
        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_KEY,
            api_version=AZURE_OPENAI_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
        self.deployment = AZURE_OPENAI_DEPLOYMENT

    def generate_answer(self, prompt: str, max_tokens: int = 300, context_docs: list[dict] = None):
        """
        Erzeugt eine Antwort mit Azure OpenAI (GPT).
        """
        context_text = ""
        
        if context_docs is not None:
            context_text = "\n".join(
                [f"- {doc['content']}" for doc in context_docs]
                )
            prompt = (
                f"\n{context_text}\nAnhand dieser Dokumente "
                f"beantworte die Frage: \nFrage: {prompt}"
            )
        
        response = self.client.chat.completions.create(
            max_completion_tokens=max_tokens,
            model=self.deployment,
            messages=[
                {"role": "system",
                    "content": "Du bist ein hilfreicher KI Assistent"},
                {"role": "user", "content": prompt}
            ],
            presence_penalty=0.0,
            frequency_penalty=0.0,
            top_p=1.0,
            temperature=1.0
        )

        return response.choices[0].message.content
