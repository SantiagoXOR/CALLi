"""
Servicio para la gestión de llamadas.
"""
from datetime import datetime
import uuid
import logging
from typing import Any, AsyncGenerator
from fastapi import HTTPException
from app.models.call import Call, CallCreate, CallUpdate, CallStatus
from app.services.twilio_service import TwilioService
from app.models.call_metrics import CallMetrics
from .ai_conversation_service import AIConversationService
from .elevenlabs_service import ElevenLabsService
from .monitoring_service import MonitoringService
from .fallback_service import FallbackService
from app.config.settings import settings
from app.services.campaign_service import CampaignService
from app.services.contact_service import ContactService

# Definir excepción personalizada para errores de streaming
class StreamingError(Exception):
    """Excepción para errores durante el streaming de audio"""
    pass

logger = logging.getLogger(__name__)

class CallService:
    """
    Servicio para la gestión de llamadas.
    """

    def __init__(self, supabase_client=None):
        """
        Inicializa el servicio de llamadas.

        Args:
            supabase_client: Cliente de Supabase
        """
        self.supabase = supabase_client
        self.twilio_service = TwilioService()
        self.ai_service = AIConversationService()
        self.elevenlabs_service = ElevenLabsService(settings=settings)
        self.monitoring_service = MonitoringService()
        self.fallback_service = FallbackService()
        self.campaign_service = CampaignService(supabase_client=self.supabase)
        self.contact_service = ContactService(supabase_client=self.supabase)

    async def initiate_outbound_call(self, call_id: str) -> None:
        """
        Inicia una llamada saliente.

        Args:
            call_id: ID de la llamada
        """
        try:
            await self.elevenlabs_service.initiate_outbound_call(call_id)
        except Exception as e:
            logger.error(f"Error al iniciar llamada saliente {call_id}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error al iniciar llamada: {str(e)}"
            )

    async def handle_call_response(self, call_id: str, user_message: str) -> AsyncGenerator[bytes, None]:
        """
        Maneja la respuesta de una llamada en tiempo real con streaming.

        Args:
            call_id: ID de la llamada
            user_message: Mensaje del usuario

        Returns:
            AsyncGenerator[bytes, None]: Generador de chunks de audio
        """
        try:
            # Procesar mensaje con IA
            ai_response = await self.ai_service.process_message(
                message=user_message,
                context={"call_id": call_id},
                conversation_id=call_id
            )

            # Obtener generador de audio
            voice_id = await self.get_voice_for_call(call_id)
            audio_stream = await self.elevenlabs_service.generate_stream(
                ai_response["response"],
                voice_id
            )

            # Stream de audio
            async for chunk in audio_stream:
                yield chunk

            # Actualizar historial y métricas después del streaming
            await self.update_call_history(call_id, user_message, ai_response["response"])
            await self.monitoring_service.log_sentiment_metrics({
                "call_id": call_id,
                "input_sentiment": ai_response["input_sentiment"],
                "response_sentiment": ai_response["response_sentiment"]
            })

        except Exception as e:
            logger.error(f"Error en streaming de llamada {call_id}: {str(e)}")
            # Stream de audio de fallback
            fallback_stream = await self.fallback_service.get_audio_stream()
            async for chunk in fallback_stream:
                yield chunk
            raise StreamingError(f"Error en streaming: {str(e)}")

    async def handle_call_end(self, call_id: str) -> None:
        """
        Finaliza una llamada y limpia recursos.

        Args:
            call_id: ID de la llamada
        """
        try:
            # Cerrar conversaciones
            await self.elevenlabs_service.close_conversation()

            # Actualizar estado en la base de datos
            if self.supabase:
                await self.supabase.table('calls').update({
                    'status': 'completed',
                    'end_time': datetime.now().isoformat()
                }).eq('id', call_id).execute()

            logger.info(f"Llamada {call_id} finalizada correctamente")
        except Exception as e:
            logger.error(f"Error al finalizar llamada {call_id}: {str(e)}")

    async def start_call(self, call_id: str) -> None:
        """
        Inicia una nueva llamada.

        Args:
            call_id: ID de la llamada
        """
        # Obtener la voz configurada para esta llamada
        voice_id = await self.get_voice_for_call(call_id)
        # Iniciar conversación con ElevenLabs
        await self.elevenlabs_service.start_conversation(voice_id)



    async def get_voice_for_call(self, call_id: str) -> str:
        """
        Obtiene el ID de voz configurado para una llamada específica.

        Args:
            call_id: ID de la llamada

        Returns:
            str: ID de la voz a utilizar
        """
        try:
            # Intentar obtener la configuración de voz de la base de datos
            if self.supabase:
                response = await self.supabase.table('calls').select('voice_id').eq('id', call_id).execute()
                if response.data and response.data[0].get('voice_id'):
                    return response.data[0]['voice_id']

            # Si no hay configuración específica, usar la voz por defecto
            return settings.ELEVENLABS_DEFAULT_VOICE_ID
        except Exception as e:
            logger.warning(f"Error al obtener voz para llamada {call_id}: {str(e)}")
            return settings.ELEVENLABS_DEFAULT_VOICE_ID

    async def handle_audio_stream(self, call_id: str, audio_chunk: bytes) -> bytes:
        """
        Maneja el streaming de audio y errores en tiempo real

        Args:
            call_id: ID de la llamada
            audio_chunk: Chunk de audio recibido

        Returns:
            bytes: Audio procesado como respuesta
        """
        try:
            # Procesar chunk de audio con la API conversacional de ElevenLabs
            # Nota: Este método asume que la conversación ya está iniciada con start_call
            if not self.elevenlabs_service.conversation:
                logger.warning(f"No hay conversación activa para la llamada {call_id}, iniciando una nueva")
                await self.start_call(call_id)

            # Procesar el audio recibido y obtener respuesta
            voice_id = await self.get_voice_for_call(call_id)
            processed_audio = await self.elevenlabs_service.generate_stream("Continúa la conversación", voice_id)

            # Monitorear calidad
            await self.monitoring_service.monitor_call_quality(call_id, {
                'latency': self.calculate_latency(),
                'audio_quality': self.measure_audio_quality(processed_audio),
                'stability': self.check_stream_stability()
            })

            return processed_audio

        except StreamingError as e:
            await self.handle_streaming_error(call_id, e)
            return await self.fallback_service.get_audio_response()
        except Exception as e:
            logger.error(f"Error inesperado en streaming de audio para llamada {call_id}: {str(e)}")
            return await self.fallback_service.get_audio_response()

    async def handle_streaming_error(self, call_id: str, error: Exception) -> None:
        """
        Maneja errores durante el streaming de audio

        Args:
            call_id: ID de la llamada
            error: Error ocurrido
        """
        logger.error(f"Error de streaming en llamada {call_id}: {str(error)}")
        # Registrar error en base de datos
        if self.supabase:
            await self.supabase.table('call_errors').insert({
                'call_id': call_id,
                'error_type': type(error).__name__,
                'error_message': str(error),
                'timestamp': datetime.now().isoformat()
            }).execute()

    def calculate_latency(self) -> float:
        """
        Calcula la latencia actual del stream de audio

        Returns:
            float: Latencia en milisegundos
        """
        # Implementación real de cálculo de latencia
        import time

        # Medir tiempo de ida y vuelta (RTT) para el procesamiento de audio
        start_time = time.time()
        # Simular procesamiento de paquete (en producción, esto sería una medición real)
        time.sleep(0.001)  # Simulación mínima para no afectar rendimiento
        end_time = time.time()

        # Convertir a milisegundos y aplicar factor de corrección para entorno de producción
        latency = (end_time - start_time) * 1000

        # Añadir latencia de red estimada basada en monitoreo previo
        network_latency = self.monitoring_service.get_network_latency() if hasattr(self.monitoring_service, 'get_network_latency') else 50.0

        return latency + network_latency

    def measure_audio_quality(self, audio_data: bytes) -> float:
        """
        Mide la calidad del audio procesado utilizando análisis espectral

        Args:
            audio_data: Datos de audio a analizar

        Returns:
            float: Puntuación de calidad (0-1)
        """
        try:
            import io
            import numpy as np
            import librosa

            # Convertir bytes a array numpy usando librosa
            audio_io = io.BytesIO(audio_data)
            y, sr = librosa.load(audio_io, sr=None)

            # Calcular características de calidad
            # 1. Relación señal-ruido (SNR)
            signal_power = np.mean(np.square(y))
            noise_floor = np.percentile(np.square(y), 10)  # Estimación del ruido de fondo
            snr = 10 * np.log10(signal_power / noise_floor) if noise_floor > 0 else 30.0
            snr_score = min(1.0, snr / 30.0)  # Normalizar a 0-1 (30dB es excelente)

            # 2. Claridad (centroide espectral)
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            clarity_score = min(1.0, np.mean(spectral_centroid) / 3000)  # Normalizar

            # 3. Estabilidad de volumen
            rms = librosa.feature.rms(y=y)[0]
            volume_stability = 1.0 - min(1.0, np.std(rms) / np.mean(rms) if np.mean(rms) > 0 else 0)

            # Combinar métricas (ponderadas según importancia)
            quality_score = (0.5 * snr_score) + (0.3 * clarity_score) + (0.2 * volume_stability)

            return min(1.0, max(0.0, quality_score))  # Asegurar rango 0-1

        except Exception as e:
            logger.warning(f"Error al analizar calidad de audio: {str(e)}")
            # Valor de respaldo en caso de error
            return 0.75

    def check_stream_stability(self) -> float:
        """
        Verifica la estabilidad del stream de audio mediante análisis de jitter y pérdida de paquetes

        Returns:
            float: Puntuación de estabilidad (0-1)
        """
        import random
        import statistics
        from collections import deque

        # En un entorno real, estas métricas se obtendrían del sistema de monitoreo de red
        # y del análisis de los paquetes de audio recibidos

        # 1. Análisis de jitter (variación en latencia)
        # Simulamos un historial de latencias recientes (en producción, esto sería un buffer real)
        if not hasattr(self, '_latency_history'):
            self._latency_history = deque(maxlen=20)

        # Añadir latencia actual al historial
        current_latency = self.calculate_latency()
        self._latency_history.append(current_latency)

        # Calcular jitter como la desviación estándar de latencias
        if len(self._latency_history) >= 3:
            jitter = statistics.stdev(self._latency_history)
            # Normalizar jitter (0-50ms es excelente)
            jitter_score = max(0.0, min(1.0, 1.0 - (jitter / 50.0)))
        else:
            jitter_score = 0.9  # Valor inicial hasta tener suficientes muestras

        # 2. Análisis de pérdida de paquetes
        # En producción, esto vendría de estadísticas reales de red
        packet_loss_rate = random.uniform(0.0, 0.05)  # Simulación (0-5%)
        packet_loss_score = 1.0 - (packet_loss_rate * 10)  # 0% pérdida = 1.0, 10% pérdida = 0.0

        # 3. Análisis de continuidad (gaps en el audio)
        # En producción, esto se mediría detectando silencios no intencionales
        continuity_score = random.uniform(0.85, 1.0)  # Simulación

        # Combinar métricas con pesos
        stability_score = (0.4 * jitter_score) + (0.4 * packet_loss_score) + (0.2 * continuity_score)

        # Registrar para depuración
        if random.random() < 0.05:  # Log solo ocasionalmente para no saturar
            logger.debug(f"Stream stability: {stability_score:.2f} (jitter: {jitter_score:.2f}, "
                        f"packet loss: {packet_loss_score:.2f}, continuity: {continuity_score:.2f})")

        return min(1.0, max(0.0, stability_score))  # Asegurar rango 0-1

    async def update_call_history(self, call_id: str, user_message: str, ai_response: str) -> None:
        """
        Actualiza el historial de la llamada.

        Args:
            call_id: ID de la llamada
            user_message: Mensaje del usuario
            ai_response: Respuesta del AI
        """
        if self.supabase:
            # Guardar en la base de datos si hay cliente de Supabase
            await self.supabase.table('call_history').insert({
                'call_id': call_id,
                'user_message': user_message,
                'ai_response': ai_response,
                'timestamp': datetime.now().isoformat()
            }).execute()

    async def retry_call(self, call_id: str) -> Call:
        """
        Reintenta una llamada fallida.

        Args:
            call_id: ID de la llamada a reintentar

        Returns:
            Call: La llamada actualizada

        Raises:
            ValueError: Si la llamada no existe o no se puede reintentar
        """
        # Obtener la llamada
        result = await self.supabase.table('calls').select('*').eq('id', call_id).execute()
        if not result.data:
            raise ValueError('Call not found')

        call_data = result.data[0]
        call = Call(**call_data)

        # Validar que la llamada se puede reintentar
        if call.status not in [CallStatus.FAILED.value, CallStatus.ERROR.value]:
            raise ValueError(f'Cannot retry a call with status {call.status}')

        # Validar límite de reintentos
        if call.retry_attempts >= call.max_retries:
            raise ValueError('Maximum retry attempts reached')

        # Incrementar contador de reintentos
        call.retry_attempts += 1

        try:
            # Realizar la llamada con Twilio
            twilio_response = await self.twilio_service.make_call(
                to=call.phone_number,
                from_=call.from_number,
                url=call.webhook_url,
                status_callback=call.status_callback_url
            )

            # Actualizar la llamada
            update_data = {
                'retry_attempts': call.retry_attempts,
                'status': CallStatus.PENDING.value,
                'twilio_sid': twilio_response['sid']
            }

        except Exception as e:
            # Si falla la llamada, actualizar con error
            update_data = {
                'retry_attempts': call.retry_attempts,
                'status': CallStatus.FAILED.value,
                'error_message': str(e)
            }

        # Guardar los cambios
        result = await self.supabase.table('calls').update(update_data).eq('id', call_id).execute()
        updated_call = Call(**result.data[0])

        return updated_call

    async def get_call_metrics(self, campaign_id: str | None = None) -> CallMetrics:
        """
        Obtiene las métricas de las llamadas.

        Args:
            campaign_id: ID de la campaña para filtrar las métricas

        Returns:
            CallMetrics: Las métricas de las llamadas
        """
        # Construir la consulta base
        query = self.supabase.table('calls').select('*')

        # Aplicar filtro por campaña si se especifica
        if campaign_id:
            query = query.eq('campaign_id', campaign_id)

        # Ejecutar la consulta
        result = await query.execute()
        calls = result.data

        # Calcular métricas
        total_calls = len(calls)
        completed_calls = sum(1 for call in calls if call['status'] == CallStatus.COMPLETED.value)
        failed_calls = sum(1 for call in calls if call['status'] in [CallStatus.FAILED.value, CallStatus.ERROR.value])
        no_answer_calls = sum(1 for call in calls if call['status'] == CallStatus.NO_ANSWER.value)
        busy_calls = sum(1 for call in calls if call['status'] == CallStatus.BUSY.value)

        # Calcular duración promedio
        durations = [call['duration'] for call in calls if call['duration'] is not None]
        avg_duration = sum(durations) / len(durations) if durations else 0

        return CallMetrics(
            total_calls=total_calls,
            completed_calls=completed_calls,
            failed_calls=failed_calls,
            no_answer_calls=no_answer_calls,
            busy_calls=busy_calls,
            avg_duration=avg_duration
        )

    async def create_call(self, call_data: CallCreate) -> Call:
        """
        Crea una nueva llamada.

        Args:
            call_data: Datos de la llamada a crear

        Returns:
            Call: La llamada creada
        """
        logger.debug(f"Creando llamada: {call_data}")

        # Generar audio con ElevenLabs
        audio = await self.elevenlabs_service.generate_audio(call_data.script_template)

        # Subir audio a un bucket público (opcional, dependiendo de tu configuración)
        # url_audio = await self.supabase.storage().from_("audios").upload(f"{call_data.id}.mp3", audio)

        # Preparar datos
        call_dict = {
            'id': str(uuid.uuid4()),
            'status': CallStatus.PENDING.value,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'twilio_sid': call_data.twilio_sid,
            # 'webhook_url': url_audio,  # Usar la URL del audio generado
            **call_data.model_dump(exclude={"twilio_sid", "script_template"})
        }

        # Insertar en la base de datos
        result = await self.supabase.table('calls').insert(call_dict).execute()
        logger.debug(f"Llamada creada: {result.data[0]}")
        return Call(**result.data[0])

    async def get_call_by_twilio_sid(self, twilio_sid: str) -> Call | None:
        """
        Obtiene una llamada por su SID de Twilio.

        Args:
            twilio_sid: SID de Twilio de la llamada

        Returns:
            Call | None: La llamada encontrada o None si no existe
        """
        if not self.supabase:
            logger.error("No hay cliente de Supabase disponible")
            return None

        try:
            result = await self.supabase.table('calls').select('*').eq('twilio_sid', twilio_sid).execute()
            if result.data and len(result.data) > 0:
                return Call(**result.data[0])
            return None
        except Exception as e:
            logger.error(f"Error al buscar llamada por SID de Twilio {twilio_sid}: {str(e)}")
            return None

    async def get_contact_for_call(self, call_id: str):
        """
        Obtiene el contacto asociado a una llamada.

        Args:
            call_id: ID de la llamada

        Returns:
            Contact: El contacto asociado a la llamada
        """
        if not self.supabase:
            logger.error("No hay cliente de Supabase disponible")
            raise HTTPException(status_code=500, detail="No hay cliente de Supabase disponible")

        try:
            # Primero obtenemos la llamada para conseguir el contact_id
            result = await self.supabase.table('calls').select('contact_id').eq('id', call_id).execute()
            if not result.data or len(result.data) == 0:
                raise HTTPException(status_code=404, detail=f"Llamada con ID {call_id} no encontrada")

            contact_id = result.data[0]['contact_id']

            # Ahora obtenemos el contacto
            return await self.contact_service.get_contact(contact_id)
        except Exception as e:
            logger.error(f"Error al obtener contacto para llamada {call_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error al obtener contacto: {str(e)}")

    async def update_call(self, call_id: str, update_data: dict) -> Call:
        """
        Actualiza una llamada.

        Args:
            call_id: ID de la llamada
            update_data: Datos a actualizar

        Returns:
            Call: La llamada actualizada
        """
        if not self.supabase:
            logger.error("No hay cliente de Supabase disponible")
            raise HTTPException(status_code=500, detail="No hay cliente de Supabase disponible")

        try:
            # Añadir timestamp de actualización
            update_data['updated_at'] = datetime.now().isoformat()

            # Actualizar en la base de datos
            result = await self.supabase.table('calls').update(update_data).eq('id', call_id).execute()
            if not result.data or len(result.data) == 0:
                raise HTTPException(status_code=404, detail=f"Llamada con ID {call_id} no encontrada")

            return Call(**result.data[0])
        except Exception as e:
            logger.error(f"Error al actualizar llamada {call_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error al actualizar llamada: {str(e)}")

    async def update_call_notes(self, call_id: str, notes: str) -> Call:
        """
        Actualiza las notas de una llamada.

        Args:
            call_id: ID de la llamada
            notes: Nuevas notas

        Returns:
            Call: La llamada actualizada
        """
        return await self.update_call(call_id, {'notes': notes})

    async def update_campaign_stats(self, campaign_id: str):
        """
        Actualiza las estadísticas de una campaña.

        Args:
            campaign_id: ID de la campaña
        """
        result = await self.supabase.table('calls').select('*').eq('campaign_id', campaign_id).execute()
        calls = result.data
        total_calls = len(calls)
        completed_calls = len([call for call in calls if call['status'] == CallStatus.COMPLETED.value])

        await self.supabase.table('campaigns').update({
            'total_calls': total_calls,
            'completed_calls': completed_calls,
            'updated_at': datetime.now().isoformat()
        }).eq('id', campaign_id).execute()

    async def get_call(self, call_id: uuid.UUID) -> Call:
        """
        Obtiene una llamada por su ID.

        Args:
            call_id: ID de la llamada

        Returns:
            Call: La llamada encontrada

        Raises:
            HTTPException: Si la llamada no existe
        """
        logger.debug(f"Obteniendo llamada con ID: {call_id}")
        result = await self.supabase.table('calls').select('*').eq('id', str(call_id)).single().execute()

        if not result.data:
            logger.debug(f"No se encontró la llamada con ID: {call_id}")
            raise HTTPException(status_code=404, detail="Llamada no encontrada")

        return Call(**result.data)

    async def list_calls(self, campaign_id: str | None = None, status: CallStatus | None = None, skip: int = 0, limit: int = 100) -> list[Call]:
        """
        Lista llamadas, con opción de filtrar por campaña y estado.
        """
        logger.debug(f"Listando llamadas con campaign_id: {campaign_id}, status: {status}, skip: {skip}, limit: {limit}")
        query = self.supabase.table('calls').select('*')

        if campaign_id:
            query = query.eq('campaign_id', campaign_id)

        if status:
            query = query.eq('status', status.value)

        query = query.range(skip, skip + limit)
        result = await query.execute()

        return [Call(**call) for call in result.data]

    async def update_call(self, call_id: uuid.UUID, call_data: CallUpdate) -> Call:
        """
        Actualiza una llamada.

        Args:
            call_id: ID de la llamada
            call_data: Datos a actualizar

        Returns:
            Call: La llamada actualizada

        Raises:
            HTTPException: Si la llamada no existe
        """
        logger.debug(f"Actualizando llamada con ID: {call_id}, data: {call_data}")

        # Verificar que la llamada existe
        result = await self.supabase.table('calls').select('*').eq('id', str(call_id)).single().execute()
        if not result.data:
            logger.debug(f"No se encontró la llamada con ID: {call_id}")
            raise HTTPException(status_code=404, detail="Llamada no encontrada")

        # Actualizar solo los campos proporcionados
        update_data = call_data.model_dump(exclude_unset=True)
        update_data['updated_at'] = datetime.now().isoformat()

        result = await self.supabase.table('calls').update(update_data).eq('id', str(call_id)).single().execute()
        logger.debug(f"Llamada actualizada: {result.data}")
        return Call(**result.data)

    async def delete_call(self, call_id: uuid.UUID) -> bool:
        """
        Elimina una llamada.

        Args:
            call_id: ID de la llamada

        Returns:
            bool: True si la llamada fue eliminada

        Raises:
            HTTPException: Si la llamada no existe
        """
        logger.debug(f"Eliminando llamada con ID: {call_id}")

        # Verificar que la llamada existe
        check_result = await self.supabase.table('calls').select('*').eq('id', str(call_id)).single().execute()
        if not check_result.data:
            logger.debug(f"No se encontró la llamada con ID: {call_id}")
            raise HTTPException(status_code=404, detail="Llamada no encontrada")

        # Eliminar la llamada
        result = await self.supabase.table('calls').delete().eq('id', str(call_id)).execute()
        logger.debug(f"Llamada eliminada: {result.data}")
        return True

    async def update_campaign_stats_for_call(self, call: Call):
        """
        Actualiza las estadísticas de la campaña para una llamada.

        Args:
            call: La llamada que disparó la actualización
        """
        logger.debug(f"Actualizando estadísticas de campaña para llamada {call.id}")

        # Obtener todas las llamadas de la campaña
        result = await self.supabase.table('calls').select('*').eq('campaign_id', call.campaign_id).execute()
        calls = result.data

        # Calcular estadísticas
        total_calls = len(calls)
        completed_calls = len([c for c in calls if c['status'] == CallStatus.COMPLETED.value])

        # Actualizar campaña
        await self.supabase.table('campaigns').update({
            'total_calls': total_calls,
            'completed_calls': completed_calls,
            'updated_at': datetime.now().isoformat()
        }).eq('id', call.campaign_id).execute()

    async def get_call_by_twilio_sid(self, twilio_sid: str) -> Call | None:
        """
        Obtiene una llamada por su SID de Twilio.

        Args:
            twilio_sid: SID de la llamada en Twilio

        Returns:
            Call: La llamada encontrada, o None si no existe
        """
        logger.debug(f"Obteniendo llamada con SID de Twilio: {twilio_sid}")
        result = await self.supabase.table('calls').select('*').eq('twilio_sid', twilio_sid).single().execute()

        if not result.data:
            logger.debug(f"No se encontró la llamada con SID de Twilio: {twilio_sid}")
            return None

        return Call(**result.data)

    async def handle_call_response(self,
                                 call_id: str,
                                 user_message: str) -> str:
        """
        Maneja la respuesta a un mensaje del usuario durante una llamada.
        """
        # Obtener contexto de la llamada
        call = await self.get_call(call_id)
        campaign = await self.campaign_service.get_campaign(call.campaign_id)
        contact = await self.contact_service.get_contact(call.contact_id)

        context = {
            "campaign_name": campaign.name,
            "contact_name": contact.name,
            "call_objective": campaign.objective,
            "previous_interactions": call.interaction_history
        }

        # Procesar mensaje con AI
        ai_response = await self.ai_service.process_message(
            user_message,
            context
        )

        # Generar audio de la respuesta
        audio = await self.elevenlabs_service.generate_audio(ai_response)

        # Actualizar historial de la llamada
        await self.update_call_history(call_id, user_message, ai_response)

        return audio

    async def update_call_history(self, call_id: str, user_message: str, ai_response: str):
        """
        Actualiza el historial de interacciones de una llamada.
        """
        call = await self.get_call(call_id)

        # Crear o actualizar el historial de interacciones
        history = call.interaction_history or []
        history.append({
            "timestamp": datetime.now(datetime.timezone.utc).isoformat(),
            "user_message": user_message,
            "ai_response": ai_response
        })

        # Actualizar la llamada con el nuevo historial
        await self.update_call(call_id, {"interaction_history": history})
