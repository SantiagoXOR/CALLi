from hvac import Client
from app.config.settings import Settings
import os
import logging

logger = logging.getLogger(__name__)

class SecretsManager:
    def __init__(self, settings: Settings):
        self.client = Client(
            url=settings.VAULT_ADDR,
            token=self._get_vault_token()
        )
        
    def _get_vault_token(self) -> str:
        # Preferir token file sobre variable de entorno
        token_file = "/run/secrets/vault-token"
        if os.path.exists(token_file):
            with open(token_file, 'r') as f:
                return f.read().strip()
        return os.environ.get("VAULT_TOKEN")

    async def get_elevenlabs_credentials(self) -> dict:
        try:
            secret = self.client.secrets.kv.v2.read_secret_version(
                path="elevenlabs",
                mount_point="kv"
            )
            return secret["data"]["data"]
        except Exception as e:
            logger.error(f"Error accessing Vault: {e}")
            raise

# Import settings here to avoid circular dependency issues if secrets_manager was imported elsewhere first
from app.config.settings import settings 
secrets_manager = SecretsManager(settings=settings)
