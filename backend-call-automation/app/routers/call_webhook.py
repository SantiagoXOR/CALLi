# backend-call-automation/app/routers/call_webhook.py

import json
from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import StreamingResponse  # Importar StreamingResponse

from app.config.dependencies import get_call_service

# Asume que tienes un sistema de dependencias para obtener CallService
from app.services.call_service import CallService, StreamingError
from app.utils.logger import get_logger  # Asume un logger configurado

logger = get_logger(__name__)
router = APIRouter()


@router.post(
    "/webhook", tags=["Webhooks"]
)  # Asegúrate que la ruta coincida con la configurada en ElevenLabsService
async def handle_call_webhook(
    request: Request,
    call_service: CallService = Depends(get_call_service),  # Inyecta CallService
):
    """
    Endpoint para recibir y manejar eventos del webhook de ElevenLabs/Twilio.
    Espera recibir eventos de llamada y devuelve audio en streaming cuando es necesario.
    """
    payload = {}
    content_type = request.headers.get("Content-Type", "").lower()
    call_id = "unknown_call"  # Default call_id

    try:
        # 1. Parsear Payload (JSON o Form-Data)
        if "application/json" in content_type:
            payload = await request.json()
        else:
            form_data = await request.form()
            payload = dict(form_data)
        logger.debug(f"Webhook payload recibido: {payload}")

        # 2. Extraer Información Clave (los nombres pueden variar)
        call_sid = payload.get("CallSid") or payload.get("call_sid")
        speech_result = payload.get("SpeechResult") or payload.get("speech_result")
        digits = payload.get("Digits") or payload.get("digits")
        call_status = payload.get("CallStatus") or payload.get("call_status")
        metadata = payload.get("metadata", {})
        # Intenta parsear metadata si es string JSON
        if isinstance(metadata, str):
            try:
                metadata = json.loads(metadata)
            except:
                metadata = {}

        # Usar CallSid como identificador principal
        call_id = call_sid if call_sid else metadata.get("conversation_tracking_id", "unknown_call")
        user_input = speech_result if speech_result else digits

        logger.info(
            f"Webhook para call_id: {call_id}, Status: {call_status}, Input: '{user_input}'"
        )

        # 3. Manejar Fin de Llamada
        if call_status in ["completed", "failed", "busy", "no-answer", "canceled"]:
            logger.info(f"Llamada {call_id} finalizada con estado: {call_status}. Limpiando.")
            # Ejecutar limpieza en segundo plano para no bloquear la respuesta
            # background_tasks.add_task(call_service.handle_call_end, call_id) # Si usas BackgroundTasks
            await call_service.handle_call_end(call_id)  # Corregido: Pasar solo call_id
            return Response(content="", status_code=200)

        # 4. Manejar Input del Usuario
        if user_input:
            logger.info(f"Procesando entrada de usuario para {call_id}: '{user_input}'")

            # Llamar a handle_call_response para obtener el generador de audio
            audio_stream_generator: AsyncGenerator[bytes, None] = call_service.handle_call_response(
                call_id=call_id, user_message=user_input
            )

            # Devolver una StreamingResponse que consuma el generador
            logger.info(f"Iniciando streaming de audio para {call_id}")
            return StreamingResponse(
                content=audio_stream_generator,
                media_type="audio/mpeg",  # O el formato que genere ElevenLabs (mp3, wav, etc.)
            )

        # 5. Manejar Otros Eventos
        logger.info(
            f"Evento intermedio para llamada {call_id}, estado: {call_status}. No se requiere acción."
        )
        # No se necesita devolver audio, respuesta vacía está bien.
        return Response(content="", status_code=200)

    except StreamingError as e:
        # Error específico durante la generación del stream (ya se intentó devolver fallback)
        logger.error(f"Error de streaming manejado para call_id {call_id}: {e}")
        # Devolver respuesta vacía o error 500
        return Response(content="", status_code=500)
    except Exception as e:
        logger.exception(f"Error fatal procesando webhook para call_id {call_id}: {e!s}")
        # Devolver una respuesta genérica de error 500
        return Response(content="", status_code=500)


# Asegúrate de incluir este router en tu app principal con el prefijo correcto:
# from app.routers import call_webhook


# app.include_router(call_webhook.router, prefix="/api/v1/calls") # Ajusta el prefijo
