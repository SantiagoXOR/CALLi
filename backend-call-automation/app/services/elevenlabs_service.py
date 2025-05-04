"""Servicio para la integración con la API de ElevenLabs para síntesis de voz."""

import asyncio
import time
from collections.abc import AsyncGenerator
from typing import Any

from httpx import AsyncClient

from app.config.secrets import secrets_manager
from app.config.settings import settings

# Import metrics
from app.monitoring.elevenlabs_metrics import (
    elevenlabs_audio_quality_score,
    elevenlabs_errors_total,
    elevenlabs_generation_duration_seconds,
    elevenlabs_pool_connections_active,
    elevenlabs_pool_size,
    elevenlabs_pool_usage_ratio,
    elevenlabs_request_duration_seconds,
    elevenlabs_requests_total,
)
from app.services.audio_cache_service import audio_cache_service
from app.utils.connection_pool import ConnectionPool
from app.utils.decorators import with_retry
from app.utils.logging_config import ElevenLabsLogger

# Instantiate the specific logger for this service
logger = ElevenLabsLogger()


class ElevenLabsAPIError(Exception):
    """Excepción personalizada para errores de la API de ElevenLabs"""


class ElevenLabsService:
    """Servicio para generar audio a partir de texto utilizando ElevenLabs."""

    def __init__(self) -> None:
        """
        Inicializa el servicio de ElevenLabs.

        Configura el pool de conexiones y las métricas iniciales.
        """
        self.conversation = None
        self.api_key = None
        pool_max_size = 10  # Default if setting fails
        try:
            pool_max_size = settings.ELEVENLABS_MAX_CONNECTIONS
            self._pool: ConnectionPool[Any] = ConnectionPool(
                max_size=pool_max_size,
                timeout=settings.ELEVENLABS_POOL_TIMEOUT,
                max_retries=settings.ELEVENLABS_MAX_RETRIES,
            )
            # Set initial pool size metric
            elevenlabs_pool_size.set(pool_max_size)
            logger.log_info(
                method="__init__",
                message=f"ElevenLabsService iniciado con pool size {pool_max_size}",
            )
        except AttributeError as e:
            logger.log_error(
                method="__init__",
                error=e,
                context={
                    "message": "Failed to read ElevenLabs settings for ConnectionPool. Using defaults."
                },
            )
            self._pool = ConnectionPool()  # Fallback to defaults
            elevenlabs_pool_size.set(10)  # Set default size metric
            logger.log_info(
                method="__init__", message="ElevenLabsService iniciado con pool size default"
            )
        # Initialize active connections metric
        elevenlabs_pool_connections_active.set(0)

    async def initiate_outbound_call(
        self,
        to_number: str,
        prompt: str | None = None,
        voice_id: str = "default_voice",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:  # Retorna un diccionario con la respuesta de la API
        """
        Inicia una llamada saliente usando la API de ElevenLabs.

        Args:
            to_number: Número de teléfono destino
            prompt: Mensaje inicial opcional
            voice_id: ID de la voz a usar
            metadata: Metadatos adicionales para la llamada

        Returns:
            Dict con la respuesta de la API

        Raises:
            ElevenLabsAPIError: Si hay un error en la API
        """
        method_name = "initiate_outbound_call"
        start_time = time.time()
        params = {"to_number": to_number, "voice_id": voice_id, "has_prompt": prompt is not None}

        url = "https://api.elevenlabs.io/v1/conversations/twilio/outbound-call"

        payload = {
            "to_number": to_number,
            "voice_id": voice_id,
            "model_id": getattr(settings, "ELEVENLABS_MODEL_ID", "eleven_multilingual_v2"),
            "twilio_account_sid": settings.TWILIO_ACCOUNT_SID,
            "twilio_auth_token": settings.TWILIO_AUTH_TOKEN,
            "from_number": getattr(settings, "TWILIO_FROM_NUMBER", settings.TWILIO_PHONE_NUMBER),
            "webhook_url": f"{getattr(settings, 'APP_BASE_URL', settings.APP_URL)}/api/v1/calls/webhook",
            "metadata": metadata or {},
        }

        if prompt:
            payload["prompt"] = prompt

        headers = {
            "xi-api-key": self.api_key
            or (await secrets_manager.get_elevenlabs_credentials())["api_key"],
            "Content-Type": "application/json",
        }

        with elevenlabs_request_duration_seconds.labels(method=method_name).time():
            try:
                elevenlabs_pool_connections_active.inc()
                elevenlabs_pool_usage_ratio.set(
                    elevenlabs_pool_connections_active._value.get()
                    / elevenlabs_pool_size._value.get()
                )

                async with self._pool.acquire() as session:
                    async with AsyncClient() as client:
                        response = await client.post(url, json=payload, headers=headers)

                        if response.status_code != 200:
                            error_msg = response.json().get("error", "Unknown error")
                            logger.log_error(
                                method=method_name, error=Exception(error_msg), context=params
                            )
                            raise ElevenLabsAPIError(f"Error initiating call: {error_msg}")

                        result = response.json()
                        duration = time.time() - start_time
                        logger.log_api_call(
                            method=method_name,
                            params=params,
                            duration=duration,
                            success=True,
                            response_info={"call_id": result.get("call_id")},
                        )
                        elevenlabs_requests_total.labels(method=method_name, status="success").inc()
                        # Convertir explícitamente a dict[str, Any]
                        response_dict: dict[str, Any] = result
                        return response_dict

            except Exception as e:
                duration = time.time() - start_time
                error_type = type(e).__name__
                logger.log_error(method=method_name, error=e, context=params)
                logger.log_api_call(
                    method=method_name, params=params, duration=duration, success=False
                )
                elevenlabs_requests_total.labels(method=method_name, status="error").inc()
                elevenlabs_errors_total.labels(error_type=error_type).inc()
                raise ElevenLabsAPIError(f"Failed to initiate call: {e!s}")
            finally:
                elevenlabs_pool_connections_active.dec()
                elevenlabs_pool_usage_ratio.set(
                    elevenlabs_pool_connections_active._value.get()
                    / elevenlabs_pool_size._value.get()
                )

    @with_retry(max_attempts=3, base_wait=1.0)
    async def generate_stream(
        self, text: str, voice_id: str = "default_voice", language: str = "es"
    ) -> AsyncGenerator[bytes, None]:
        """
        Genera un stream de audio a partir de texto usando la API de streaming de ElevenLabs.
        Utiliza caché para optimizar el rendimiento y reducir llamadas a la API.

        Args:
            text: Texto a convertir en audio
            voice_id: ID de la voz a usar
            language: Idioma del texto (por defecto: es)

        Returns:
            AsyncGenerator[bytes, None]: Generador de chunks de audio

        Raises:
            ElevenLabsAPIError: Si hay un error en la API
        """
        method_name = "generate_stream"
        start_time = time.time()
        params = {"text_length": len(text), "voice_id": voice_id, "language": language}

        # Verificar si el audio está en caché
        cached_file_path = await audio_cache_service.get_from_cache(text, voice_id, language)
        if cached_file_path:
            logger.log_info(
                method=method_name,
                message=f"Audio encontrado en caché: {cached_file_path}",
                context={"from_cache": True, "text_length": len(text)},
            )

            # Leer el archivo de caché y devolverlo como stream
            try:
                with open(cached_file_path, "rb") as f:
                    # Leer en chunks para simular streaming
                    chunk_size = 4096  # 4KB chunks
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        yield chunk

                duration = time.time() - start_time
                logger.log_api_call(
                    method=method_name,
                    params=params,
                    duration=duration,
                    success=True,
                    response_info={"from_cache": True, "file_path": cached_file_path},
                )
                return
            except Exception as e:
                # Si hay un error al leer el caché, continuar con la API
                logger.log_error(
                    method=method_name,
                    error=e,
                    context={"from_cache": True, "file_path": cached_file_path},
                )
                # Continuar con la generación desde la API

        # Si no está en caché o hubo un error, generar desde la API
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

        payload = {
            "text": text,
            "model_id": getattr(settings, "ELEVENLABS_MODEL_ID", "eleven_multilingual_v2"),
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        }

        headers = {
            "xi-api-key": self.api_key
            or (await secrets_manager.get_elevenlabs_credentials())["api_key"],
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        }

        with elevenlabs_generation_duration_seconds.labels(method=method_name).time():
            try:
                elevenlabs_pool_connections_active.inc()
                elevenlabs_pool_usage_ratio.set(
                    elevenlabs_pool_connections_active._value.get()
                    / elevenlabs_pool_size._value.get()
                )

                # Recolectar todos los chunks para guardar en caché
                all_chunks = []

                async with self._pool.acquire() as session:
                    async with AsyncClient() as client:
                        async with client.stream(
                            "POST", url, json=payload, headers=headers
                        ) as response:
                            if response.status_code != 200:
                                error_msg = await response.json()
                                error_msg = error_msg.get("error", "Unknown error")
                                logger.log_error(
                                    method=method_name, error=Exception(error_msg), context=params
                                )
                                raise ElevenLabsAPIError(
                                    f"Error generating audio stream: {error_msg}"
                                )

                            async for chunk in response.aiter_bytes():
                                all_chunks.append(chunk)
                                yield chunk

                            duration = time.time() - start_time

                        # Evaluar calidad del audio generado (métrica simulada)
                        quality_score = 0.95  # En producción, usar análisis real
                        # Usar observe en lugar de set para histogramas
                        elevenlabs_audio_quality_score.observe(quality_score)

                        # Guardar en caché si hay chunks
                        if all_chunks:
                            audio_data = b"".join(all_chunks)
                            audio_size = len(audio_data)

                            # Guardar en caché de forma asíncrona
                            asyncio.create_task(
                                audio_cache_service.save_to_cache(
                                    text, voice_id, audio_data, language
                                )
                            )

                            logger.log_api_call(
                                method=method_name,
                                params=params,
                                duration=duration,
                                success=True,
                                response_info={"audio_size": audio_size, "cached": True},
                            )
                        else:
                            logger.log_api_call(
                                method=method_name,
                                params=params,
                                duration=duration,
                                success=True,
                                response_info={"audio_size": 0, "cached": False},
                            )

                        elevenlabs_requests_total.labels(method=method_name, status="success").inc()

            except Exception as e:
                duration = time.time() - start_time
                error_type = type(e).__name__
                logger.log_error(method=method_name, error=e, context=params)
                logger.log_api_call(
                    method=method_name, params=params, duration=duration, success=False
                )
                elevenlabs_requests_total.labels(method=method_name, status="error").inc()
                elevenlabs_errors_total.labels(error_type=error_type).inc()
                raise ElevenLabsAPIError(f"Failed to generate audio stream: {e!s}")
            finally:
                elevenlabs_pool_connections_active.dec()
                elevenlabs_pool_usage_ratio.set(
                    elevenlabs_pool_connections_active._value.get()
                    / elevenlabs_pool_size._value.get()
                )

    async def start_conversation(
        self, voice_id: str = "default_voice"
    ) -> dict[str, Any]:  # Retorna un diccionario con la información de la conversación
        """
        Inicia una nueva conversación con ElevenLabs.

        Args:
            voice_id: ID de la voz a usar

        Returns:
            Dict con la información de la conversación
        """
        method_name = "start_conversation"
        start_time = time.time()

        url = "https://api.elevenlabs.io/v1/conversations"

        payload = {
            "voice_id": voice_id,
            "model_id": getattr(settings, "ELEVENLABS_MODEL_ID", "eleven_multilingual_v2"),
            "name": f"Conversation-{int(time.time())}",
        }

        headers = {
            "xi-api-key": self.api_key
            or (await secrets_manager.get_elevenlabs_credentials())["api_key"],
            "Content-Type": "application/json",
        }

        try:
            async with AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers)

                if response.status_code != 200:
                    error_msg = response.json().get("error", "Unknown error")
                    logger.log_error(
                        method=method_name,
                        error=Exception(error_msg),
                        context={"voice_id": voice_id},
                    )
                    raise ElevenLabsAPIError(f"Error starting conversation: {error_msg}")

                result = response.json()
                self.conversation = result.get("conversation_id")

                duration = time.time() - start_time
                logger.log_api_call(
                    method=method_name,
                    params={"voice_id": voice_id},
                    duration=duration,
                    success=True,
                    response_info={"conversation_id": self.conversation},
                )
                # Convertir explícitamente a dict[str, Any]
                response_dict: dict[str, Any] = result
                return response_dict

        except Exception as e:
            duration = time.time() - start_time
            logger.log_error(method=method_name, error=e, context={"voice_id": voice_id})
            logger.log_api_call(
                method=method_name, params={"voice_id": voice_id}, duration=duration, success=False
            )
            raise ElevenLabsAPIError(f"Failed to start conversation: {e!s}")

    async def generate_audio(self, text: str, voice_id: str = "default_voice") -> bytes:
        """
        Genera audio a partir de texto usando la API de ElevenLabs.

        Args:
            text: Texto a convertir en audio
            voice_id: ID de la voz a usar

        Returns:
            bytes: Datos de audio generados

        Raises:
            ElevenLabsAPIError: Si hay un error en la API
        """
        method_name = "generate_audio"
        start_time = time.time()
        params = {"text_length": len(text), "voice_id": voice_id}

        # Verificar si el audio está en caché
        cached_file_path = await audio_cache_service.get_from_cache(text, voice_id)
        if cached_file_path:
            logger.log_info(
                method=method_name,
                message=f"Audio encontrado en caché: {cached_file_path}",
                context={"from_cache": True, "text_length": len(text)},
            )

            # Leer el archivo de caché y devolverlo
            try:
                with open(cached_file_path, "rb") as f:
                    audio_data = f.read()

                duration = time.time() - start_time
                logger.log_api_call(
                    method=method_name,
                    params=params,
                    duration=duration,
                    success=True,
                    response_info={"from_cache": True, "file_path": cached_file_path},
                )
                return audio_data
            except Exception as e:
                # Si hay un error al leer el caché, continuar con la API
                logger.log_error(
                    method=method_name,
                    error=e,
                    context={"from_cache": True, "file_path": cached_file_path},
                )
                # Continuar con la generación desde la API

        # Si no está en caché o hubo un error, generar desde la API
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        payload = {
            "text": text,
            "model_id": getattr(settings, "ELEVENLABS_MODEL_ID", "eleven_multilingual_v2"),
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        }

        headers = {
            "xi-api-key": self.api_key
            or (await secrets_manager.get_elevenlabs_credentials())["api_key"],
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        }

        with elevenlabs_generation_duration_seconds.labels(method=method_name).time():
            try:
                elevenlabs_pool_connections_active.inc()
                elevenlabs_pool_usage_ratio.set(
                    elevenlabs_pool_connections_active._value.get()
                    / elevenlabs_pool_size._value.get()
                )

                async with self._pool.acquire() as session:
                    async with AsyncClient() as client:
                        response = await client.post(url, json=payload, headers=headers)

                        if response.status_code != 200:
                            error_msg = response.json().get("error", "Unknown error")
                            logger.log_error(
                                method=method_name, error=Exception(error_msg), context=params
                            )
                            raise ElevenLabsAPIError(f"Error generating audio: {error_msg}")

                        # Leer el contenido de la respuesta
                        audio_data = response.read()
                        if asyncio.iscoroutine(audio_data):
                            audio_data = await audio_data
                        audio_size = len(audio_data)

                        # Guardar en caché de forma asíncrona
                        asyncio.create_task(
                            audio_cache_service.save_to_cache(text, voice_id, audio_data)
                        )

                        duration = time.time() - start_time
                        logger.log_api_call(
                            method=method_name,
                            params=params,
                            duration=duration,
                            success=True,
                            response_info={"audio_size": audio_size, "cached": True},
                        )

                        elevenlabs_requests_total.labels(method=method_name, status="success").inc()
                        return audio_data

            except Exception as e:
                duration = time.time() - start_time
                error_type = type(e).__name__
                logger.log_error(method=method_name, error=e, context=params)
                logger.log_api_call(
                    method=method_name, params=params, duration=duration, success=False
                )
                elevenlabs_requests_total.labels(method=method_name, status="error").inc()
                elevenlabs_errors_total.labels(error_type=error_type).inc()
                raise ElevenLabsAPIError(f"Failed to generate audio: {e!s}")
            finally:
                elevenlabs_pool_connections_active.dec()
                elevenlabs_pool_usage_ratio.set(
                    elevenlabs_pool_connections_active._value.get()
                    / elevenlabs_pool_size._value.get()
                )

    async def close_conversation(self) -> None:
        """
        Cierra la conversación actual con ElevenLabs.

        Si no hay una conversación activa, registra un mensaje informativo y retorna.
        """
        if not self.conversation:
            logger.log_info(method="close_conversation", message="No active conversation to close")
            return  # Salir temprano si no hay conversación activa

        method_name = "close_conversation"
        start_time = time.time()

        url = f"https://api.elevenlabs.io/v1/conversations/{self.conversation}/close"

        headers = {
            "xi-api-key": self.api_key
            or (await secrets_manager.get_elevenlabs_credentials())["api_key"],
            "Content-Type": "application/json",
        }

        try:
            async with AsyncClient() as client:
                response = await client.post(url, headers=headers)

                if response.status_code != 200:
                    error_msg = response.json().get("error", "Unknown error")
                    logger.log_error(
                        method=method_name,
                        error=Exception(error_msg),
                        context={"conversation_id": self.conversation},
                    )
                    raise ElevenLabsAPIError(f"Error closing conversation: {error_msg}")

                duration = time.time() - start_time
                logger.log_api_call(
                    method=method_name,
                    params={"conversation_id": self.conversation},
                    duration=duration,
                    success=True,
                )

                # Limpiar la conversación actual
                self.conversation = None

        except Exception as e:
            duration = time.time() - start_time
            logger.log_error(
                method=method_name, error=e, context={"conversation_id": self.conversation}
            )
            logger.log_api_call(
                method=method_name,
                params={"conversation_id": self.conversation},
                duration=duration,
                success=False,
            )
            # Limpiar la conversación incluso en caso de error
            self.conversation = None
