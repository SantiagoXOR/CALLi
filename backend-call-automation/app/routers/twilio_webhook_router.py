"""
Router para los webhooks de Twilio.
"""
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.request_validator import RequestValidator
import logging
from typing import Dict, Any, Optional
import json

from app.config.settings import settings
from app.services.twilio_service import TwilioService
from app.services.call_service import CallService
from app.models.call import CallStatus
from app.dependencies.service_dependencies import get_call_service, get_twilio_service

# Configurar logger
logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(
    prefix="/webhooks/twilio",
    tags=["webhooks"],
    responses={404: {"description": "Not found"}},
)

async def validate_twilio_request(request: Request) -> bool:
    """
    Valida que la solicitud provenga de Twilio.
    
    Args:
        request: Objeto Request de FastAPI
        
    Returns:
        bool: True si la solicitud es válida, False en caso contrario
    """
    # Obtener la firma de Twilio del encabezado
    twilio_signature = request.headers.get("X-Twilio-Signature")
    if not twilio_signature:
        logger.warning("Solicitud sin firma de Twilio")
        return False
    
    # Construir la URL completa
    url = str(request.url)
    
    # Obtener los parámetros de la solicitud
    form_data = await request.form()
    params = dict(form_data)
    
    # Validar la firma
    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
    is_valid = validator.validate(url, params, twilio_signature)
    
    if not is_valid:
        logger.warning(f"Firma de Twilio inválida para URL: {url}")
    
    return is_valid

@router.post("/", response_class=PlainTextResponse)
async def twilio_webhook(
    request: Request,
    call_service: CallService = Depends(get_call_service)
):
    """
    Webhook principal para manejar llamadas de Twilio.
    Genera respuestas TwiML para controlar el flujo de la llamada.
    """
    # Validar que la solicitud provenga de Twilio
    if not settings.APP_DEBUG and not await validate_twilio_request(request):
        raise HTTPException(status_code=403, detail="Solicitud no autorizada")
    
    # Obtener datos del formulario
    form_data = await request.form()
    call_sid = form_data.get("CallSid")
    
    logger.info(f"Webhook recibido para llamada {call_sid}")
    
    # Buscar la llamada en la base de datos
    call = await call_service.get_call_by_twilio_sid(call_sid)
    if not call:
        logger.error(f"Llamada con SID {call_sid} no encontrada")
        raise HTTPException(status_code=404, detail="Llamada no encontrada")
    
    # Actualizar estado de la llamada a IN_PROGRESS
    await call_service.update_call(
        call.id, 
        {"status": CallStatus.IN_PROGRESS}
    )
    
    # Obtener información del contacto
    contact = await call_service.get_contact_for_call(call.id)
    
    # Generar respuesta TwiML
    response = VoiceResponse()
    
    # Saludar al contacto
    response.say(
        f"Hola {contact.name}, le llamamos de {settings.APP_NAME}.",
        voice="woman",
        language="es-ES"
    )
    
    # Reproducir el script de la llamada
    response.say(
        call.script_template,
        voice="woman",
        language="es-ES"
    )
    
    # Recopilar entrada del usuario
    gather = Gather(
        input="dtmf speech",
        timeout=5,
        num_digits=1,
        action=f"{settings.APP_URL}/api/webhooks/twilio/gather",
        method="POST"
    )
    
    gather.say(
        "Presione 1 si está interesado, 2 si desea que le llamemos más tarde, o diga 'interesado' para recibir más información.",
        voice="woman",
        language="es-ES"
    )
    
    response.append(gather)
    
    # Si no hay respuesta
    response.say(
        "No hemos recibido respuesta. Gracias por su tiempo, le llamaremos en otro momento.",
        voice="woman",
        language="es-ES"
    )
    
    response.hangup()
    
    return Response(content=str(response), media_type="application/xml")

@router.post("/gather", response_class=PlainTextResponse)
async def twilio_gather_webhook(
    request: Request,
    call_service: CallService = Depends(get_call_service)
):
    """
    Webhook para manejar la entrada del usuario durante una llamada.
    """
    # Validar que la solicitud provenga de Twilio
    if not settings.APP_DEBUG and not await validate_twilio_request(request):
        raise HTTPException(status_code=403, detail="Solicitud no autorizada")
    
    # Obtener datos del formulario
    form_data = await request.form()
    call_sid = form_data.get("CallSid")
    digits = form_data.get("Digits")
    speech_result = form_data.get("SpeechResult")
    
    logger.info(f"Gather recibido para llamada {call_sid}: Digits={digits}, Speech={speech_result}")
    
    # Buscar la llamada en la base de datos
    call = await call_service.get_call_by_twilio_sid(call_sid)
    if not call:
        logger.error(f"Llamada con SID {call_sid} no encontrada")
        raise HTTPException(status_code=404, detail="Llamada no encontrada")
    
    # Generar respuesta TwiML
    response = VoiceResponse()
    
    # Procesar la entrada del usuario
    user_input = digits or speech_result
    
    if digits == "1" or (speech_result and "interesado" in speech_result.lower()):
        # Usuario interesado
        response.say(
            "Gracias por su interés. Un representante se pondrá en contacto con usted pronto para brindarle más información.",
            voice="woman",
            language="es-ES"
        )
        
        # Actualizar la llamada con la respuesta del usuario
        await call_service.update_call_notes(
            call.id, 
            "Usuario interesado. Requiere seguimiento."
        )
        
    elif digits == "2":
        # Usuario quiere que le llamen más tarde
        response.say(
            "Entendido. Le llamaremos en otro momento más conveniente. Gracias por su tiempo.",
            voice="woman",
            language="es-ES"
        )
        
        # Actualizar la llamada con la respuesta del usuario
        await call_service.update_call_notes(
            call.id, 
            "Usuario solicita ser contactado más tarde."
        )
        
    else:
        # Respuesta no reconocida
        response.say(
            "No hemos podido entender su respuesta. Gracias por su tiempo, le llamaremos en otro momento.",
            voice="woman",
            language="es-ES"
        )
        
        # Actualizar la llamada con la respuesta del usuario
        await call_service.update_call_notes(
            call.id, 
            f"Respuesta no reconocida: {user_input}"
        )
    
    response.hangup()
    
    return Response(content=str(response), media_type="application/xml")

@router.post("/status", response_class=PlainTextResponse)
async def call_status_webhook(
    request: Request,
    call_service: CallService = Depends(get_call_service)
):
    """
    Webhook para recibir actualizaciones de estado de llamadas de Twilio.
    """
    # Validar que la solicitud provenga de Twilio
    if not settings.APP_DEBUG and not await validate_twilio_request(request):
        raise HTTPException(status_code=403, detail="Solicitud no autorizada")
    
    # Obtener datos del formulario
    form_data = await request.form()
    call_sid = form_data.get("CallSid")
    call_status = form_data.get("CallStatus")
    call_duration = form_data.get("CallDuration")
    recording_url = form_data.get("RecordingUrl")
    error_message = form_data.get("ErrorMessage")
    
    logger.info(f"Status webhook recibido para llamada {call_sid}: Status={call_status}")
    
    # Buscar la llamada en la base de datos
    call = await call_service.get_call_by_twilio_sid(call_sid)
    if not call:
        logger.error(f"Llamada con SID {call_sid} no encontrada")
        raise HTTPException(status_code=404, detail="Llamada no encontrada")
    
    # Mapear el estado de Twilio al estado de nuestra aplicación
    status_mapping = {
        "queued": CallStatus.PENDING,
        "ringing": CallStatus.IN_PROGRESS,
        "in-progress": CallStatus.IN_PROGRESS,
        "completed": CallStatus.COMPLETED,
        "busy": CallStatus.BUSY,
        "failed": CallStatus.FAILED,
        "no-answer": CallStatus.NO_ANSWER,
        "canceled": CallStatus.CANCELLED
    }
    
    new_status = status_mapping.get(call_status, call.status)
    
    # Preparar datos para actualizar
    update_data = {"status": new_status}
    
    if call_duration:
        update_data["duration"] = int(call_duration)
    
    if recording_url:
        update_data["recording_url"] = recording_url
    
    if error_message:
        update_data["error_message"] = error_message
    
    # Actualizar la llamada
    await call_service.update_call(call.id, update_data)
    
    # Si la llamada ha terminado, actualizar las estadísticas de la campaña
    if call_status in ["completed", "busy", "failed", "no-answer", "canceled"]:
        await call_service.update_campaign_stats(call.campaign_id)
    
    return Response(content="", status_code=200)
