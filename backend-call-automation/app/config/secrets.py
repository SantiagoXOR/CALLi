import logging
import os
from typing import Any

from hvac import Client

# Import settings here to avoid circular dependency issues
from app.config.settings import Settings, settings

logger = logging.getLogger(__name__)


class SecretsManager:
    """
    Gestor de secretos para la aplicación.

    Esta clase se encarga de obtener secretos desde HashiCorp Vault.
    """

    def __init__(self, settings: Settings) -> None:
        """
        Inicializa el gestor de secretos.

        Args:
            settings: Configuración de la aplicación
        """
        self.client = Client(url=settings.VAULT_ADDR, token=self._get_vault_token())

    def _get_vault_token(self) -> str:
        """
        Obtiene el token de Vault desde un archivo o variable de entorno.

        Returns:
            str: Token de Vault
        """
        # Preferir token file sobre variable de entorno
        token_file = os.environ.get("VAULT_TOKEN_FILE", "/run/secrets/vault-token")
        if os.path.exists(token_file):
            with open(token_file) as f:
                return f.read().strip()
        return os.environ.get("VAULT_TOKEN", "")

    async def get_elevenlabs_credentials(self) -> dict[str, Any]:
        """
        Obtiene las credenciales de ElevenLabs desde Vault.

        Returns:
            Dict[str, Any]: Diccionario con las credenciales de ElevenLabs

        Raises:
            Exception: Si hay un error al acceder a Vault
        """
        try:
            secret = self.client.secrets.kv.v2.read_secret_version(
                path="elevenlabs", mount_point="kv"
            )
            return secret["data"]["data"]
        except Exception:
            logger.exception("Error accessing Vault")
            raise


# Crear una instancia global del gestor de secretos
secrets_manager = SecretsManager(settings=settings)
