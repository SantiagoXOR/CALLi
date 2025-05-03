"""Servicio de respaldo (fallback) para manejar errores y proporcionar alternativas cuando el servicio principal falla."""

import asyncio
import logging
import os
from collections.abc import AsyncGenerator
from datetime import datetime, timedelta

from elevenlabs.client import ElevenLabs  # Importar la clase correcta
from prometheus_client import Counter, Gauge, Histogram

logger = logging.getLogger(__name__)


class FallbackService:
    """
    Servicio de respaldo que implementa el patrón Circuit Breaker para manejar fallos.

         Este servicio proporciona respuestas alternativas cuando el servicio principal
         experimenta problemas, evitando fallos en cascada y mejorando la resiliencia del sistema.
    """

    def __init__(self) -> None:  # Corrected indentation
        """Inicializa el servicio de fallback.

        Configura las respuestas predeterminadas para diferentes tipos de campañas,
        inicializa el cliente de métricas y establece el estado inicial del circuit breaker.
        """
        self.client = ElevenLabs(
            api_key=os.environ.get("ELEVENLABS_API_KEY")
        )  # Usar la clase correcta
        self.fallback_responses = {
            "sales": "Lo siento, estoy experimentando dificultades técnicas. ¿Podría contactar con uno de nuestros representantes de ventas?",
            "support": "Disculpe la interrupción. Para continuar con su soporte, le conectaré con un agente humano.",
            "survey": "Perdón por los inconvenientes. ¿Podríamos reagendar esta encuesta para otro momento?",
        }
        self.default_fallback = (
            "Lo siento, estoy experimentando problemas técnicos. ¿Podría intentarlo más tarde?"
        )
        self.circuit_breaker_state = "CLOSED"
        self.consecutive_failures = 0
        self.failure_threshold = 5
        self.retry_timeout = 30
        self.last_failure_time = None
        self.default_voice = "Bella"

        # Inicializar métricas de Prometheus
        self.elevenlabs_failures_total = Counter(
            "elevenlabs_failures_total", "Total de fallos en ElevenLabs"
        )
        self.elevenlabs_api_latency = Histogram(
            "elevenlabs_api_latency_seconds", "Latencia de la API de ElevenLabs"
        )
        self.circuit_breaker_state_gauge = Gauge(
            "circuit_breaker_state", "Estado del Circuit Breaker (0: cerrado, 1: abierto)"
        )

    async def handle_failure(self, error: Exception) -> None:
        """
        Implementa el Circuit Breaker Pattern para manejar fallos

        Args:
            error: Excepción que causó el fallo
        """
        self.consecutive_failures += 1
        self.last_failure_time = datetime.now()

        # Registrar métricas para monitoreo
        self.elevenlabs_failures_total.inc()

        logger.warning(
            f"Fallo detectado: {error!s}. Fallos consecutivos: {self.consecutive_failures}"
        )

        # Verificar si debemos abrir el circuito
        if (
            self.circuit_breaker_state == "CLOSED"
            and self.consecutive_failures >= self.failure_threshold
        ):
            logger.warning(
                f"Circuit Breaker abierto después de {self.consecutive_failures} fallos consecutivos"
            )
            self.circuit_breaker_state = "OPEN"
            self.circuit_breaker_state_gauge.set(1)

        # Registrar el error para análisis posterior
        await self._log_failure(error)

    async def _log_failure(self, error: Exception) -> None:
        """
        Registra información detallada sobre el fallo para análisis

        Args:
            error: Excepción que causó el fallo
        """
        # En un entorno real, esto registraría en una base de datos o sistema de monitoreo
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "circuit_state": self.circuit_breaker_state,
        }

        logger.error(f"Error detallado: {error_info}")

    async def check_circuit_state(self) -> bool:
        """
        Verifica el estado actual del circuit breaker y determina si se puede proceder.

        Implementa la lógica del patrón Circuit Breaker para evitar llamadas a servicios
        que están experimentando fallos, permitiendo un tiempo de recuperación.

        Returns:
            bool: True si se puede proceder con la operación, False si está bloqueada
        """
        # Si el circuito está cerrado, permitir la operación
        if self.circuit_breaker_state == "CLOSED":
            return True

        # Si el circuito está abierto, verificar si ha pasado el tiempo de espera
        if self.last_failure_time and (datetime.now() - self.last_failure_time) > timedelta(
            seconds=self.retry_timeout
        ):
            logger.info(
                f"Cambiando Circuit Breaker a HALF_OPEN después de {self.retry_timeout} segundos"
            )
            self.circuit_breaker_state = "HALF_OPEN"
            self.circuit_breaker_state_gauge.set(0.5)
        else:
            return False  # Aún en periodo de espera

        # Si está en HALF_OPEN, permitir un intento de prueba
        return self.circuit_breaker_state == "HALF_OPEN"

    async def record_success(self) -> None:
        """
        Registra una operación exitosa y actualiza el estado del circuit breaker.

        Este método se llama cuando una operación se completa con éxito, lo que puede
        llevar a cerrar el circuit breaker si estaba abierto, permitiendo que el sistema
        vuelva a su funcionamiento normal después de un periodo de fallos.
        """
        # Resetear contador de fallos consecutivos
        self.consecutive_failures = 0

        # Si el circuito estaba abierto, cerrarlo
        if self.circuit_breaker_state == "OPEN":
            logger.info("Circuit Breaker cerrado después de operación exitosa")
            self.circuit_breaker_state = "CLOSED"
            self.circuit_breaker_state_gauge.set(0)

    async def get_fallback_response(self, campaign_type: str, context: dict[str, str]) -> str:
        """
        Obtiene una respuesta de fallback apropiada según el tipo de campaña

        Args:
            campaign_type: Tipo de campaña
            context: Contexto adicional

        Returns:
            str: Mensaje de respuesta para fallback
        """
        return self.fallback_responses.get(campaign_type, self.default_fallback)

    async def get_audio_response(
        self, campaign_type: str | None = None, context: dict | None = None
    ) -> bytes:
        """
        Genera una respuesta de audio para casos de error, respetando el estado del circuit breaker

        Args:
            campaign_type: Tipo de campaña (opcional)
            context: Contexto adicional (opcional)

        Returns:
            bytes: Audio generado como respuesta de fallback
        """
        # Verificar estado del circuit breaker
        can_proceed = await self.check_circuit_state()

        if not can_proceed:
            logger.warning("Circuit breaker abierto, usando respuesta pregrabada")
            return self._get_prerecorded_fallback()

        try:
            # Obtener texto de respuesta
            text = await self.get_fallback_response(campaign_type or "general", context or {})

            # Generar audio con voz predeterminada
            with self.elevenlabs_api_latency.time():
                audio = self.client.generate(text=text, voice=self.default_voice)

            # Registrar éxito para el circuit breaker
            await self.record_success()

            return audio

        except Exception as e:
            # Registrar fallo en el circuit breaker
            await self.handle_failure(e)

            # Si falla la generación, devolver audio pregrabado
            return self._get_prerecorded_fallback()

    async def get_audio_stream(self) -> AsyncGenerator[bytes, None]:
        """
        Proporciona un generador asíncrono de chunks de audio para streaming en caso de fallback.

        Este método es útil para mantener la continuidad del streaming cuando el servicio principal falla.

        Returns:
            AsyncGenerator[bytes, None]: Generador de chunks de audio
        """
        try:
            # Obtener el audio completo
            audio_data = await self.get_audio_response()

            # Simular streaming dividiendo en chunks
            chunk_size = 4096  # 4KB chunks
            total_chunks = len(audio_data) // chunk_size + (
                1 if len(audio_data) % chunk_size > 0 else 0
            )

            logger.info(f"Streaming audio de fallback en {total_chunks} chunks")

            # Entregar los chunks uno por uno
            for i in range(0, len(audio_data), chunk_size):
                chunk = audio_data[i : i + chunk_size]
                yield chunk

                # Pequeña pausa para simular streaming real
                await asyncio.sleep(0.01)

        except Exception as e:
            logger.error(f"Error en streaming de audio de fallback: {e!s}")
            # En caso de error, devolver un chunk vacío
            yield b""

    def _get_prerecorded_fallback(self) -> bytes:
        """
        Obtiene una respuesta de audio pregrabada como último recurso de fallback.

        Este método se utiliza cuando todas las demás opciones de generación de audio
        han fallado, proporcionando una respuesta pregrabada para mantener la continuidad
        de la llamada.

        Returns:
            bytes: Audio pregrabado con mensaje de fallback
        """
        # En un entorno real, esto cargaría un archivo de audio pregrabado
        # Por ahora, generamos uno simple con ElevenLabs
        try:
            audio = self.client.generate(text=self.default_fallback, voice=self.default_voice)
            return audio
        except Exception as e:
            logger.error(f"Error al generar audio de fallback: {e!s}")
            # Devolver un archivo de audio vacío como último recurso
            return b""
