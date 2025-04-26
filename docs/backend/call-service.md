# Servicio de Llamadas

## Visión General

El `CallService` es un componente central del sistema de automatización de llamadas que gestiona el ciclo de vida completo de las llamadas telefónicas. Este servicio coordina la interacción entre Twilio para la telefonía, ElevenLabs para la síntesis de voz, y el servicio de IA para la generación de conversaciones naturales.

## Funcionalidades Principales

### 1. Gestión de Llamadas

- **Iniciar llamadas**: Crear y programar nuevas llamadas
- **Monitorear estados**: Seguimiento del estado de las llamadas en tiempo real
- **Finalizar llamadas**: Terminar llamadas y registrar resultados
- **Reintentar llamadas**: Gestionar reintentos automáticos para llamadas fallidas

### 2. Procesamiento de Conversaciones

- **Manejo de respuestas**: Procesar respuestas del usuario en tiempo real
- **Generación de audio**: Convertir texto a voz utilizando ElevenLabs
- **Integración con IA**: Coordinar con el servicio de IA para generar respuestas contextuales
- **Streaming de audio**: Transmitir audio generado en tiempo real

### 3. Monitoreo y Métricas

- **Registro de métricas**: Recopilar métricas de llamadas (duración, calidad, etc.)
- **Alertas**: Generar alertas para problemas durante las llamadas
- **Logging**: Registro detallado de eventos de llamadas
- **Trazabilidad**: Seguimiento del flujo de ejecución de las llamadas

### 4. Gestión de Errores

- **Manejo de excepciones**: Gestionar errores durante las llamadas
- **Fallback**: Implementar mecanismos de respaldo en caso de fallos
- **Reintentos**: Configurar políticas de reintentos para operaciones fallidas
- **Degradación elegante**: Mantener funcionalidad básica en caso de fallos parciales

## Implementación

### Clase Principal

```python
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
```

### Métodos Principales

#### Gestión de Llamadas

```python
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

    # Preparar datos
    call_dict = {
        'id': str(uuid.uuid4()),
        'status': CallStatus.PENDING.value,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'twilio_sid': call_data.twilio_sid,
        **call_data.dict(exclude={"twilio_sid", "script_template"})
    }

    # Insertar en base de datos
    try:
        result = self.supabase.table('calls').insert(call_dict).execute()
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear la llamada"
            )
        
        # Actualizar estadísticas de campaña
        await self.campaign_service.increment_pending_calls(call_data.campaign_id)
        
        # Registrar métrica
        self.monitoring_service.metrics_client.counter("calls_created_total", 1)
        
        return Call(**result.data[0])
    except Exception as e:
        logger.error(f"Error al crear llamada: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear llamada: {str(e)}"
        )

async def get_call(self, call_id: str) -> Call:
    """
    Obtiene una llamada por su ID.
    
    Args:
        call_id: ID de la llamada
        
    Returns:
        Call: La llamada encontrada
    """
    try:
        result = self.supabase.table('calls').select('*').eq('id', call_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Llamada no encontrada"
            )
        
        return Call(**result.data[0])
    except Exception as e:
        logger.error(f"Error al obtener llamada {call_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener llamada: {str(e)}"
        )

async def update_call(self, call_id: str, call_data: CallUpdate) -> Call:
    """
    Actualiza una llamada existente.
    
    Args:
        call_id: ID de la llamada
        call_data: Datos a actualizar
        
    Returns:
        Call: La llamada actualizada
    """
    try:
        # Filtrar campos None para no sobrescribir con valores nulos
        update_data = {k: v for k, v in call_data.dict().items() if v is not None}
        update_data['updated_at'] = datetime.now().isoformat()
        
        result = self.supabase.table('calls').update(update_data).eq('id', call_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Llamada no encontrada"
            )
        
        # Si se actualiza el estado, actualizar estadísticas de campaña
        if call_data.status:
            call = Call(**result.data[0])
            await self._update_campaign_stats(call)
        
        return Call(**result.data[0])
    except Exception as e:
        logger.error(f"Error al actualizar llamada {call_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar llamada: {str(e)}"
        )
```

#### Procesamiento de Conversaciones

```python
async def initiate_outbound_call(self, call_id: str) -> None:
    """
    Inicia una llamada saliente.
    
    Args:
        call_id: ID de la llamada
    """
    try:
        # Obtener datos de la llamada
        call = await self.get_call(call_id)
        
        # Actualizar estado
        await self.update_call(call_id, CallUpdate(status=CallStatus.IN_PROGRESS))
        
        # Iniciar llamada con ElevenLabs
        await self.elevenlabs_service.initiate_outbound_call(call_id)
        
        # Registrar métrica
        self.monitoring_service.metrics_client.counter("calls_initiated_total", 1)
    except Exception as e:
        logger.error(f"Error al iniciar llamada saliente {call_id}: {str(e)}")
        
        # Actualizar estado a fallido
        await self.update_call(
            call_id, 
            CallUpdate(
                status=CallStatus.FAILED,
                error_message=str(e)
            )
        )
        
        # Intentar fallback si es posible
        try:
            await self.fallback_service.handle_call_failure(call_id, str(e))
        except Exception as fallback_error:
            logger.error(f"Error en fallback para llamada {call_id}: {str(fallback_error)}")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al iniciar llamada: {str(e)}"
        )

async def handle_call_response(self, call_id: str, user_message: str) -> AsyncGenerator[bytes, None]:
    """
    Maneja la respuesta de una llamada en tiempo real con streaming.
    
    Args:
        call_id: ID de la llamada
        user_message: Mensaje del usuario
        
    Returns:
        Generator de bytes de audio
    """
    try:
        # Obtener datos de la llamada
        call = await self.get_call(call_id)
        
        # Obtener respuesta de IA
        ai_response = await self.ai_service.get_response(
            call_id=call_id,
            user_message=user_message,
            context={
                "campaign_id": call.campaign_id,
                "contact_id": call.contact_id
            }
        )
        
        # Generar audio con streaming
        async for audio_chunk in self.elevenlabs_service.generate_audio_stream(ai_response):
            yield audio_chunk
        
        # Registrar métrica
        self.monitoring_service.metrics_client.counter("call_responses_total", 1)
    except Exception as e:
        logger.error(f"Error al manejar respuesta de llamada {call_id}: {str(e)}")
        
        # Intentar fallback
        try:
            fallback_audio = await self.fallback_service.get_fallback_audio(call_id, str(e))
            yield fallback_audio
        except Exception as fallback_error:
            logger.error(f"Error en fallback para respuesta {call_id}: {str(fallback_error)}")
            
            # Si todo falla, devolver mensaje de error genérico
            error_message = "Lo siento, estoy experimentando problemas técnicos."
            error_audio = await self.elevenlabs_service.generate_audio(error_message)
            yield error_audio
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al manejar respuesta: {str(e)}"
        )
```

#### Monitoreo y Métricas

```python
async def get_call_metrics(self, campaign_id: str = None) -> CallMetrics:
    """
    Obtiene métricas de llamadas.
    
    Args:
        campaign_id: ID de campaña opcional para filtrar
        
    Returns:
        CallMetrics: Métricas de llamadas
    """
    try:
        query = self.supabase.table('calls').select('*')
        
        if campaign_id:
            query = query.eq('campaign_id', campaign_id)
        
        result = query.execute()
        
        if not result.data:
            return CallMetrics()
        
        calls = [Call(**call) for call in result.data]
        
        # Calcular métricas
        total_calls = len(calls)
        completed_calls = len([c for c in calls if c.status == CallStatus.COMPLETED])
        failed_calls = len([c for c in calls if c.status == CallStatus.FAILED])
        no_answer_calls = len([c for c in calls if c.status == CallStatus.NO_ANSWER])
        busy_calls = len([c for c in calls if c.status == CallStatus.BUSY])
        
        # Calcular duración promedio
        durations = [c.duration for c in calls if c.duration is not None and c.status == CallStatus.COMPLETED]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return CallMetrics(
            total_calls=total_calls,
            completed_calls=completed_calls,
            failed_calls=failed_calls,
            no_answer_calls=no_answer_calls,
            busy_calls=busy_calls,
            avg_duration=avg_duration
        )
    except Exception as e:
        logger.error(f"Error al obtener métricas de llamadas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener métricas: {str(e)}"
        )
```

#### Gestión de Errores y Reintentos

```python
async def retry_failed_call(self, call_id: str) -> Call:
    """
    Reintenta una llamada fallida.
    
    Args:
        call_id: ID de la llamada
        
    Returns:
        Call: La llamada actualizada
    """
    try:
        # Obtener datos de la llamada
        call = await self.get_call(call_id)
        
        # Verificar si se puede reintentar
        if call.retry_attempts >= call.max_retries:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Se ha alcanzado el número máximo de reintentos"
            )
        
        # Incrementar contador de reintentos
        call = await self.update_call(
            call_id,
            CallUpdate(
                status=CallStatus.PENDING,
                retry_attempts=call.retry_attempts + 1
            )
        )
        
        # Programar nuevo intento
        await self.initiate_outbound_call(call_id)
        
        # Registrar métrica
        self.monitoring_service.metrics_client.counter("call_retries_total", 1)
        
        return call
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al reintentar llamada {call_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al reintentar llamada: {str(e)}"
        )

async def _update_campaign_stats(self, call: Call) -> None:
    """
    Actualiza las estadísticas de la campaña basado en el estado de la llamada.
    
    Args:
        call: Llamada actualizada
    """
    try:
        # Obtener campaña
        campaign = await self.campaign_service.get_campaign(str(call.campaign_id))
        
        # Actualizar estadísticas según el estado
        if call.status == CallStatus.COMPLETED:
            await self.campaign_service.increment_successful_calls(str(call.campaign_id))
        elif call.status == CallStatus.FAILED:
            await self.campaign_service.increment_failed_calls(str(call.campaign_id))
        elif call.status == CallStatus.PENDING:
            await self.campaign_service.increment_pending_calls(str(call.campaign_id))
    except Exception as e:
        logger.error(f"Error al actualizar estadísticas de campaña: {str(e)}")
        # No propagar la excepción para no afectar la operación principal
```

## Configuración

El servicio de llamadas se configura a través de variables de entorno y el módulo de configuración:

```python
# En app/config/settings.py
class Settings(BaseSettings):
    # Twilio Configuration
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    
    # ElevenLabs Configuration
    ELEVENLABS_API_KEY: str
    ELEVENLABS_DEFAULT_VOICE: str
    ELEVENLABS_MODEL_ID: str = "eleven_turbo_v2"
    
    # Application Configuration
    APP_BASE_URL: str
    
    # Call Configuration
    DEFAULT_CALL_TIMEOUT: int = 30
    MAX_RETRY_ATTEMPTS: int = 3
    RETRY_DELAY_MINUTES: int = 60
```

## Uso

### Inicialización

```python
# En app/main.py
from app.services.call_service import CallService
from app.config.supabase import supabase_client

call_service = CallService(supabase_client=supabase_client)
```

### Uso en Endpoints

```python
# En app/routers/calls.py
@router.post("/", response_model=Call)
async def create_call(call_data: CallCreate):
    """Crea una nueva llamada."""
    return await call_service.create_call(call_data)

@router.get("/{call_id}", response_model=Call)
async def get_call(call_id: str):
    """Obtiene una llamada por su ID."""
    return await call_service.get_call(call_id)

@router.put("/{call_id}", response_model=Call)
async def update_call(call_id: str, call_data: CallUpdate):
    """Actualiza una llamada existente."""
    return await call_service.update_call(call_id, call_data)

@router.post("/{call_id}/initiate", status_code=status.HTTP_202_ACCEPTED)
async def initiate_call(call_id: str):
    """Inicia una llamada saliente."""
    await call_service.initiate_outbound_call(call_id)
    return {"message": "Llamada iniciada correctamente"}

@router.post("/{call_id}/response")
async def handle_response(call_id: str, request: Request):
    """Maneja la respuesta de una llamada en tiempo real."""
    body = await request.json()
    user_message = body.get("message", "")
    
    return StreamingResponse(
        call_service.handle_call_response(call_id, user_message),
        media_type="audio/mpeg"
    )

@router.post("/{call_id}/retry", response_model=Call)
async def retry_call(call_id: str):
    """Reintenta una llamada fallida."""
    return await call_service.retry_failed_call(call_id)

@router.get("/metrics", response_model=CallMetrics)
async def get_metrics(campaign_id: str = None):
    """Obtiene métricas de llamadas."""
    return await call_service.get_call_metrics(campaign_id)
```

## Flujo de Llamada

1. **Creación**: Se crea una nueva llamada con `create_call`
2. **Iniciación**: Se inicia la llamada con `initiate_outbound_call`
3. **Conversación**: Se procesan las respuestas con `handle_call_response`
4. **Finalización**: Se actualiza el estado con `update_call`
5. **Métricas**: Se registran métricas con `get_call_metrics`

## Consideraciones de Rendimiento

- **Procesamiento asíncrono**: Uso de async/await para operaciones de I/O
- **Streaming de audio**: Transmisión de audio en chunks para reducir latencia
- **Caché**: Uso de caché para respuestas frecuentes
- **Monitoreo**: Registro de métricas para identificar cuellos de botella
- **Optimización de consultas**: Minimizar consultas a la base de datos

## Consideraciones de Seguridad

- **Validación de entrada**: Validación de todos los datos de entrada
- **Manejo seguro de credenciales**: Uso de variables de entorno y gestores de secretos
- **Auditoría**: Registro de acciones críticas
- **Limitación de tasa**: Implementación de rate limiting
- **Sanitización de datos**: Limpieza de datos antes de procesarlos

## Solución de Problemas

### Problemas Comunes

1. **Llamadas que no se inician**:
   - Verificar credenciales de Twilio
   - Comprobar conectividad con ElevenLabs
   - Revisar logs para errores específicos

2. **Problemas de calidad de audio**:
   - Verificar configuración de ElevenLabs
   - Comprobar ancho de banda disponible
   - Ajustar parámetros de generación de voz

3. **Errores en conversaciones**:
   - Verificar integración con el servicio de IA
   - Comprobar prompts y configuración
   - Revisar logs para errores específicos

4. **Problemas de rendimiento**:
   - Monitorear métricas de latencia
   - Verificar uso de recursos
   - Optimizar consultas y procesamiento

### Comandos Útiles

```bash
# Verificar logs
tail -f logs/call_service.log

# Monitorear métricas
curl http://localhost:8000/metrics

# Verificar estado de llamadas
curl http://localhost:8000/api/v1/calls/metrics
```

## Referencias

- [Twilio API Documentation](https://www.twilio.com/docs/api)
- [ElevenLabs API Documentation](https://elevenlabs.io/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Supabase Documentation](https://supabase.io/docs)
