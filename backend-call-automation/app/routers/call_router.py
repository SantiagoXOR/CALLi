from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, status, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from app.models.call import Call, CallCreate, CallUpdate, CallStatus, CallDetail
from app.services.call_service import CallService
from app.services.twilio_service import TwilioService
from app.config.dependencies import get_call_service, get_supabase_client, get_twilio_service
from supabase import Client as SupabaseClient

router = APIRouter(prefix="/api/calls", tags=["calls"])

@router.post("/", response_model=Call, status_code=status.HTTP_201_CREATED)
async def create_call(
    call: CallCreate,
    supabase_client: SupabaseClient = Depends(get_supabase_client), # Usar dependencia unificada
    twilio_service: TwilioService = Depends(get_twilio_service) # Usar dependencia unificada
) -> Call:
    """
    Crea una nueva llamada y la inicia con Twilio.
    """
    # twilio_response = await twilio_client.calls.create(
    #     to=call.phone_number,
    #     from_=call.from_number,
    #     url=call.webhook_url,
    #     status_callback=call.status_callback_url
    # )

    # call.twilio_sid = twilio_response.sid

    # Usar twilio_service.client en lugar de twilio_client directamente
    twilio_response = await twilio_service.client.calls.create(
        to=call.phone_number,
        from_=call.from_number,
        url=call.webhook_url,
        status_callback=call.status_callback_url
    )

    call.twilio_sid = twilio_response.sid

    call_service = CallService(supabase_client, twilio_service) # Pasar twilio_service a CallService si es necesario (verificar constructor)
    return await call_service.create_call(call)

@router.get("/{call_id}", response_model=CallDetail)
async def get_call(
    call_id: str = Path(..., description="ID de la llamada"),
    include_recordings: bool = Query(False, description="Incluir URLs de grabaciones"),
    include_transcripts: bool = Query(False, description="Incluir transcripciones"),
    call_service: CallService = Depends(get_call_service)
) -> CallDetail:
    """
    Obtiene información detallada de una llamada por su ID.

    - **call_id**: ID único de la llamada
    - **include_recordings**: Si es True, incluye URLs de grabaciones
    - **include_transcripts**: Si es True, incluye transcripciones de la llamada

    Returns:
        Información detallada de la llamada
    """
    return await call_service.get_call_detail(
        call_id=call_id,
        include_recordings=include_recordings,
        include_transcripts=include_transcripts
    )

@router.get("/", response_model=Dict[str, Any])
async def list_calls(
    campaign_id: Optional[str] = Query(None, description="Filtrar por ID de campaña"),
    status: Optional[CallStatus] = Query(None, description="Filtrar por estado de llamada"),
    contact_id: Optional[str] = Query(None, description="Filtrar por ID de contacto"),
    start_date: Optional[datetime] = Query(None, description="Filtrar desde fecha (formato ISO)"),
    end_date: Optional[datetime] = Query(None, description="Filtrar hasta fecha (formato ISO)"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    sort_by: str = Query("created_at", description="Campo para ordenar"),
    sort_order: str = Query("desc", description="Orden (asc/desc)"),
    call_service: CallService = Depends(get_call_service)
) -> Dict[str, Any]:
    """
    Lista las llamadas con filtros avanzados y paginación.

    - **campaign_id**: Filtrar por ID de campaña
    - **status**: Filtrar por estado de llamada
    - **contact_id**: Filtrar por ID de contacto
    - **start_date**: Filtrar desde fecha (formato ISO)
    - **end_date**: Filtrar hasta fecha (formato ISO)
    - **page**: Número de página (comienza en 1)
    - **page_size**: Tamaño de página (entre 1 y 100)
    - **sort_by**: Campo para ordenar (created_at, status, duration, etc.)
    - **sort_order**: Orden (asc/desc)

    Returns:
        Dict con datos de llamadas y metadatos de paginación
    """
    calls, total = await call_service.list_calls(
        campaign_id=campaign_id,
        status=status,
        contact_id=contact_id,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order
    )

    return {
        "data": calls,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size if page_size > 0 else 1
    }

@router.patch("/{call_id}/status", response_model=Call)
async def update_call_status(
    call_id: str = Path(..., description="ID de la llamada"),
    status: CallStatus = Query(..., description="Nuevo estado de la llamada"),
    duration: Optional[int] = Query(None, description="Duración en segundos"),
    recording_url: Optional[str] = Query(None, description="URL de la grabación"),
    error_message: Optional[str] = Query(None, description="Mensaje de error"),
    call_service: CallService = Depends(get_call_service)
) -> Call:
    """
    Actualiza el estado de una llamada.

    - **call_id**: ID único de la llamada
    - **status**: Nuevo estado de la llamada
    - **duration**: Duración en segundos (opcional)
    - **recording_url**: URL de la grabación (opcional)
    - **error_message**: Mensaje de error (opcional)

    Returns:
        Llamada actualizada
    """
    return await call_service.update_call_status(
        call_id=call_id,
        status=status,
        duration=duration,
        recording_url=recording_url,
        error_message=error_message
    )

@router.post("/{call_id}/cancel", response_model=Call)
async def cancel_call(
    call_id: str = Path(..., description="ID de la llamada"),
    reason: str = Query(None, description="Razón de la cancelación"),
    call_service: CallService = Depends(get_call_service),
    twilio_service: TwilioService = Depends(get_twilio_service)
) -> Call:
    """
    Cancela una llamada programada o en curso.

    - **call_id**: ID único de la llamada
    - **reason**: Razón de la cancelación (opcional)

    Returns:
        Llamada actualizada con estado cancelado
    """
    # Obtener la llamada
    call = await call_service.get_call(call_id)

    # Cancelar en Twilio si está en curso
    if call.twilio_sid and call.status in [CallStatus.in_progress, CallStatus.queued]:
        await twilio_service.cancel_call(call.twilio_sid)

    # Actualizar estado en la base de datos
    return await call_service.update_call_status(
        call_id=call_id,
        status=CallStatus.cancelled,
        error_message=reason if reason else "Cancelada manualmente"
    )

@router.post("/{call_id}/reschedule", response_model=Call)
async def reschedule_call(
    call_id: str = Path(..., description="ID de la llamada"),
    scheduled_time: datetime = Query(..., description="Nueva fecha/hora programada"),
    call_service: CallService = Depends(get_call_service)
) -> Call:
    """
    Reprograma una llamada para una fecha/hora futura.

    - **call_id**: ID único de la llamada
    - **scheduled_time**: Nueva fecha/hora programada (formato ISO)

    Returns:
        Llamada actualizada con nueva fecha programada
    """
    # Verificar que la fecha es futura
    if scheduled_time <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de reprogramación debe ser futura"
        )

    # Reprogramar la llamada
    return await call_service.reschedule_call(
        call_id=call_id,
        scheduled_time=scheduled_time
    )

@router.get("/metrics", response_model=Dict[str, Any])
async def get_call_metrics(
    campaign_id: Optional[str] = Query(None, description="Filtrar por ID de campaña"),
    start_date: Optional[datetime] = Query(None, description="Filtrar desde fecha (formato ISO)"),
    end_date: Optional[datetime] = Query(None, description="Filtrar hasta fecha (formato ISO)"),
    group_by: str = Query("day", description="Agrupar por (day, week, month)"),
    call_service: CallService = Depends(get_call_service)
) -> Dict[str, Any]:
    """
    Obtiene métricas detalladas de las llamadas.

    - **campaign_id**: Filtrar por ID de campaña (opcional)
    - **start_date**: Filtrar desde fecha (formato ISO)
    - **end_date**: Filtrar hasta fecha (formato ISO)
    - **group_by**: Agrupar por (day, week, month)

    Returns:
        Dict con métricas de llamadas
    """
    # Si no se especifica end_date, usar fecha actual
    if not end_date:
        end_date = datetime.now()

    # Si no se especifica start_date, usar 30 días antes de end_date
    if not start_date:
        start_date = end_date - timedelta(days=30)

    return await call_service.get_call_metrics(
        campaign_id=campaign_id,
        start_date=start_date,
        end_date=end_date,
        group_by=group_by
    )

@router.post("/twilio_callback", status_code=status.HTTP_200_OK)
async def twilio_callback(
    twilio_data: Dict[str, str],
    call_service: CallService = Depends(get_call_service)
) -> JSONResponse:
    """
    Endpoint para recibir las actualizaciones de estado de Twilio.

    Este endpoint procesa los callbacks de Twilio para actualizar el estado de las llamadas.
    Recibe datos como CallSid, CallStatus, CallDuration, RecordingUrl, etc.

    Returns:
        JSONResponse con confirmación de procesamiento
    """
    try:
        call_sid = twilio_data.get("CallSid")
        call_status = twilio_data.get("CallStatus")

        if not call_sid or not call_status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CallSid y CallStatus son requeridos"
            )

        # Buscar la llamada por el SID de Twilio
        call = await call_service.get_call_by_twilio_sid(call_sid)

        if not call:
            # Loguear pero no fallar, podría ser un callback para una llamada que aún no está en nuestro sistema
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"status": "warning", "message": f"Llamada con SID {call_sid} no encontrada"}
            )

        # Extraer datos adicionales
        duration = int(twilio_data.get("CallDuration", 0)) if twilio_data.get("CallDuration") else None
        recording_url = twilio_data.get("RecordingUrl")
        error_code = twilio_data.get("ErrorCode")
        error_message = twilio_data.get("ErrorMessage")

        # Mapear estado de Twilio a nuestro modelo
        status_mapping = {
            "queued": CallStatus.queued,
            "ringing": CallStatus.ringing,
            "in-progress": CallStatus.in_progress,
            "completed": CallStatus.completed,
            "busy": CallStatus.failed,
            "no-answer": CallStatus.failed,
            "canceled": CallStatus.cancelled,
            "failed": CallStatus.failed
        }

        mapped_status = status_mapping.get(call_status.lower(), CallStatus.unknown)

        # Actualizar el estado de la llamada
        await call_service.update_call_status(
            call_id=call.id,
            status=mapped_status,
            duration=duration,
            recording_url=recording_url,
            error_message=error_message if error_message else (f"Error code: {error_code}" if error_code else None)
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "success", "message": f"Llamada {call_sid} actualizada a estado {mapped_status}"}
        )

    except Exception as e:
        # Loguear el error pero devolver 200 para que Twilio no reintente
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "error", "message": f"Error procesando callback: {str(e)}"}
        )


@router.post("/{call_id}/respond", response_model=Dict[str, Any])
async def handle_call_response(
    call_id: str = Path(..., description="ID de la llamada"),
    message: Dict[str, str] = ...,
    call_service: CallService = Depends(get_call_service)
) -> Dict[str, Any]:
    """
    Endpoint para manejar respuestas durante una llamada activa.

    - **call_id**: ID único de la llamada
    - **message**: Objeto con el texto del mensaje del usuario

    Returns:
        Dict con la respuesta de audio y metadatos
    """
    try:
        if "text" not in message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El campo 'text' es requerido en el mensaje"
            )

        # Verificar que la llamada existe y está activa
        call = await call_service.get_call(call_id)
        if not call:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Llamada no encontrada"
            )

        if call.status != CallStatus.in_progress:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La llamada no está activa. Estado actual: {call.status}"
            )

        # Procesar la respuesta
        audio_response = await call_service.handle_call_response(
            call_id=call_id,
            user_message=message["text"]
        )

        return {
            "status": "success",
            "audio": audio_response,
            "call_id": call_id,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la respuesta: {str(e)}"
        )
