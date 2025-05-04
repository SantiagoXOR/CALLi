"""
Servicio para la integración con Twilio.
"""

import logging
from typing import Any

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from app.config.settings import Settings  # Importar Settings

logger = logging.getLogger(__name__)
settings = Settings()  # Instanciar Settings


class TwilioService:
    """
    Servicio para la integración con Twilio.
    """

    def __init__(self) -> None:
        """
        Inicializa el servicio de Twilio.
        """
        self.account_sid = settings.TWILIO_ACCOUNT_SID  # Usar settings
        self.auth_token = settings.TWILIO_AUTH_TOKEN  # Usar settings
        self.client = (
            Client(self.account_sid, self.auth_token)
            if self.account_sid and self.auth_token
            else None
        )

    async def make_call(
        self,
        to: str,
        from_: str,
        url: str,
        status_callback: str | None = None,
        timeout: int = 30,
    ) -> dict[str, Any]:
        """
        Realiza una llamada usando Twilio.

        Args:
            to: Número de teléfono al que se realizará la llamada
            from_: Número de teléfono desde el que se realizará la llamada
            url: URL del webhook para manejar la llamada
            status_callback: URL para recibir actualizaciones del estado de la llamada
            timeout: Tiempo máximo de espera para la llamada en segundos

        Returns:
            Dict[str, Any]: Información de la llamada creada

        Raises:
            Exception: Si hay un error al realizar la llamada
        """
        try:
            if not self.client:
                raise ValueError(
                    "Twilio client not initialized. Check TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables."
                )

            logger.debug(f"Realizando llamada a {to} desde {from_}")
            call = self.client.calls.create(
                to=to, from_=from_, url=url, status_callback=status_callback, timeout=timeout
            )

            logger.debug(f"Llamada creada con SID: {call.sid}")
            return {
                "sid": call.sid,
                "status": call.status,
                "direction": call.direction,
                "from": call.from_,
                "to": call.to,
                "duration": call.duration,
            }

        except TwilioRestException as e:
            logger.exception(f"Error de Twilio al realizar la llamada: {e!s}")
            raise Exception(f"Twilio error: {e!s}") from e

        except Exception as e:
            logger.exception(f"Error al realizar la llamada: {e!s}")
            raise
