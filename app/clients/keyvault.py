import logging
import os

from typing import Optional
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from app.config import AZURE_KEY_VAULT_URL

# ============================================
# Logging Konfiguration
# ============================================
logging.basicConfig(logging.INFO)


class AzureKeyVaultClient:
    """
    Azure Key Vault Client zum sicheren Abrufen sensibler Secrets.
    """

    def __init__(self):
        self.key_vault_url = AZURE_KEY_VAULT_URL
        if not self.key_vault_url:
            raise ValueError("AZURE_KEY_VAULT_URL nicht in der .env Datei gesetzt.")

        # Verwendung von Azure Default Credential
        #  (beispielsweise Managed Identity, CLI Login)
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(
            vault_url=self.key_vault_url, credential=self.credential
        )

    def get_secret(self, secret_name: str) -> str:
        """
        Ruft den Wert aus Azure Key Vault ab
        """
        try:
            secret = self.client.get_secret(secret_name)
            return secret.value
        except Exception as e:
            logging.error(f"Fehler beim Aufruf vom Geheimnis: {secret_name}")
            return None
