import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch, call
from datetime import datetime
from app.services.call_service import CallService, StreamingError
from app.models.call import Call, CallCreate, CallUpdate, CallStatus
from fastapi import HTTPException

@pytest.fixture
def mock_supabase():
    return MagicMock()

@pytest.fixture
def call_service(mock_supabase):
    service = CallService(supabase_client=mock_supabase)
    service.elevenlabs_service = AsyncMock()
    service.ai_service = AsyncMock()
    service.monitoring_service = AsyncMock()
    service.fallback_service = AsyncMock()
    return service

@pytest.mark.asyncio
async def test_initiate_outbound_call_success(call_service):
    call_id = "test-call-id"
    
    # Configurar el mock
    call_service.elevenlabs_service.initiate_outbound_call.return_value = None
    
    # Ejecutar la función
    await call_service.initiate_outbound_call(call_id)
    
    # Verificar que se llamó al servicio de ElevenLabs
    call_service.elevenlabs_service.initiate_outbound_call.assert_called_once_with(call_id)

@pytest.mark.asyncio
async def test_initiate_outbound_call_failure(call_service):
    call_id = "test-call-id"
    
    # Configurar el mock para lanzar una excepción
    call_service.elevenlabs_service.initiate_outbound_call.side_effect = Exception("Error de prueba")
    
    # Verificar que se lanza la excepción HTTP
    with pytest.raises(HTTPException):
        await call_service.initiate_outbound_call(call_id)

@pytest.mark.asyncio
async def test_handle_call_response_success(call_service):
    call_id = "test-call-id"
    user_message = "Hola"
    ai_response = {
        "response": "Respuesta de prueba",
        "input_sentiment": "neutral",
        "response_sentiment": "positive"
    }
    
    # Configurar mocks
    call_service.ai_service.process_message.return_value = ai_response
    call_service.get_voice_for_call = AsyncMock(return_value="voice-id")
    call_service.elevenlabs_service.generate_stream.return_value = [b"chunk1", b"chunk2"]
    
    # Ejecutar y verificar el streaming
    chunks = []
    async for chunk in await call_service.handle_call_response(call_id, user_message):
        chunks.append(chunk)
    
    assert chunks == [b"chunk1", b"chunk2"]
    call_service.monitoring_service.log_sentiment_metrics.assert_called_once()

@pytest.mark.asyncio
async def test_handle_call_response_with_error(call_service):
    call_id = "test-call-id"
    user_message = "Hola"
    
    # Configurar mock para simular error
    call_service.ai_service.process_message.side_effect = Exception("Error de prueba")
    call_service.fallback_service.get_audio_stream.return_value = [b"fallback"]
    
    # Ejecutar y verificar el fallback
    chunks = []
    with pytest.raises(StreamingError):
        async for chunk in await call_service.handle_call_response(call_id, user_message):
            chunks.append(chunk)
    
    assert chunks == [b"fallback"]

@pytest.mark.asyncio
async def test_handle_call_end_success(call_service):
    call_id = "test-call-id"
    
    # Ejecutar la función
    await call_service.handle_call_end(call_id)
    
    # Verificar que se cerraron las conversaciones
    call_service.elevenlabs_service.close_conversation.assert_called_once()
    
    # Verificar actualización en Supabase
    call_service.supabase.table.return_value.update.return_value.eq.return_value.execute.assert_called_once()

@pytest.mark.asyncio
async def test_get_voice_for_call(call_service):
    call_id = "test-call-id"
    voice_id = "test-voice-id"
    
    # Configurar mock de Supabase
    call_service.supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = \
        MagicMock(data=[{"voice_id": voice_id}])
    
    # Ejecutar y verificar
    result = await call_service.get_voice_for_call(call_id)
    assert result == voice_id

@pytest.mark.asyncio
async def test_get_voice_for_call_fallback_to_default(call_service, monkeypatch):
    call_id = "test-call-id"
    default_voice_id = "default-voice"
    
    # Configurar mock de Supabase para no devolver datos
    call_service.supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = \
        MagicMock(data=[])
        
    # Mockear settings
    monkeypatch.setattr("app.config.settings.settings.ELEVENLABS_DEFAULT_VOICE_ID", default_voice_id)
    
    # Ejecutar y verificar
    result = await call_service.get_voice_for_call(call_id)
    assert result == default_voice_id

@pytest.mark.asyncio
async def test_start_call(call_service):
    call_id = "test-call-id"
    voice_id = "test-voice-id"
    
    # Mockear get_voice_for_call
    call_service.get_voice_for_call = AsyncMock(return_value=voice_id)
    
    # Ejecutar
    await call_service.start_call(call_id)
    
    # Verificar llamadas
    call_service.get_voice_for_call.assert_called_once_with(call_id)
    call_service.elevenlabs_service.start_conversation.assert_called_once_with(voice_id)

@pytest.mark.asyncio
async def test_handle_audio_stream_success(call_service):
    call_id = "test-call-id"
    audio_chunk = b"input_chunk"
    processed_audio = b"processed_audio"
    voice_id = "test-voice-id"
    
    # Configurar mocks
    call_service.get_voice_for_call = AsyncMock(return_value=voice_id)
    call_service.elevenlabs_service.conversation = True # Simular conversación activa
    call_service.elevenlabs_service.generate_stream = AsyncMock(return_value=processed_audio)
    call_service.calculate_latency = MagicMock(return_value=100.0)
    call_service.measure_audio_quality = MagicMock(return_value=0.9)
    call_service.check_stream_stability = MagicMock(return_value=0.95)
    
    # Ejecutar
    result = await call_service.handle_audio_stream(call_id, audio_chunk)
    
    # Verificar
    assert result == processed_audio
    call_service.get_voice_for_call.assert_called_once_with(call_id)
    call_service.elevenlabs_service.generate_stream.assert_called_once_with("Continúa la conversación", voice_id)
    call_service.monitoring_service.monitor_call_quality.assert_called_once()

# Nota: Faltan pruebas para casos de error en handle_audio_stream

@pytest.mark.asyncio
async def test_update_call_history(call_service):
    call_id = "test-call-id"
    user_message = "User says something"
    ai_response = "AI responds"
    
    # Mockear get_call para devolver una llamada simulada
    mock_call = Call(id=call_id, campaign_id="camp1", contact_id="cont1", interaction_history=[])
    call_service.get_call = AsyncMock(return_value=mock_call)
    call_service.update_call = AsyncMock() # Mockear update_call para evitar llamadas reales a Supabase
    
    # Ejecutar
    await call_service.update_call_history(call_id, user_message, ai_response)
    
    # Verificar que se llamó a update_call con el historial actualizado
    call_service.update_call.assert_called_once()
    args, kwargs = call_service.update_call.call_args
    assert args[0] == call_id
    updated_history = args[1]["interaction_history"]
    assert len(updated_history) == 1
    assert updated_history[0]["user_message"] == user_message
    assert updated_history[0]["ai_response"] == ai_response
    assert "timestamp" in updated_history[0]

@pytest.mark.asyncio
async def test_create_call(call_service):
    call_data = CallCreate(
        campaign_id="camp1",
        contact_id="cont1",
        phone_number="+1234567890",
        from_number="+0987654321",
        script_template="Hello {name}",
        # twilio_sid="ACxxxx" # Opcional aquí
    )
    generated_audio = b"audio_data"
    call_id = uuid.uuid4()
    
    # Mockear dependencias
    call_service.elevenlabs_service.generate_audio.return_value = generated_audio
    # Mockear la inserción en Supabase
    mock_execute = AsyncMock()
    mock_execute.return_value = MagicMock(data=[{
        'id': str(call_id), 
        'status': CallStatus.PENDING.value, 
        'created_at': datetime.now().isoformat(), 
        'updated_at': datetime.now().isoformat(),
        'twilio_sid': None, # Asumiendo que no se pasó
        **call_data.dict(exclude={"twilio_sid", "script_template"})
    }])
    call_service.supabase.table.return_value.insert.return_value.execute = mock_execute
    
    # Ejecutar
    with patch('uuid.uuid4', return_value=call_id): # Mockear uuid.uuid4
        created_call = await call_service.create_call(call_data)
    
    # Verificar
    call_service.elevenlabs_service.generate_audio.assert_called_once_with(call_data.script_template)
    call_service.supabase.table.return_value.insert.assert_called_once()
    insert_args = call_service.supabase.table.return_value.insert.call_args[0][0]
    assert insert_args['id'] == str(call_id)
    assert insert_args['campaign_id'] == call_data.campaign_id
    assert created_call.id == str(call_id)
    assert created_call.status == CallStatus.PENDING.value

@pytest.mark.asyncio
async def test_get_call_success(call_service):
    call_id = uuid.uuid4()
    mock_call_data = {'id': str(call_id), 'status': 'completed', 'campaign_id': 'c1', 'contact_id': 'p1'}
    
    # Mockear Supabase
    mock_execute = AsyncMock()
    mock_execute.return_value = MagicMock(data=mock_call_data)
    call_service.supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute = mock_execute
    
    # Ejecutar
    call = await call_service.get_call(call_id)
    
    # Verificar
    assert call.id == str(call_id)
    assert call.status == 'completed'
    call_service.supabase.table.return_value.select.return_value.eq.assert_called_once_with('id', str(call_id))

@pytest.mark.asyncio
async def test_get_call_not_found(call_service):
    call_id = uuid.uuid4()
    
    # Mockear Supabase para no devolver datos
    mock_execute = AsyncMock()
    mock_execute.return_value = MagicMock(data=None)
    call_service.supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute = mock_execute
    
    # Ejecutar y verificar excepción
    with pytest.raises(HTTPException) as exc_info:
        await call_service.get_call(call_id)
    assert exc_info.value.status_code == 404

@pytest.mark.asyncio
async def test_update_call_success(call_service):
    call_id = uuid.uuid4()
    update_data = CallUpdate(status=CallStatus.COMPLETED)
    mock_existing_call = {'id': str(call_id), 'status': 'in_progress'}
    mock_updated_call = {'id': str(call_id), 'status': CallStatus.COMPLETED.value, 'updated_at': datetime.now().isoformat()}

    # Mockear la verificación de existencia
    mock_check_execute = AsyncMock(return_value=MagicMock(data=mock_existing_call))
    call_service.supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute = mock_check_execute

    # Mockear la actualización
    mock_update_execute = AsyncMock(return_value=MagicMock(data=mock_updated_call))
    call_service.supabase.table.return_value.update.return_value.eq.return_value.single.return_value.execute = mock_update_execute

    # Ejecutar
    updated_call = await call_service.update_call(call_id, update_data)

    # Verificar
    call_service.supabase.table.return_value.select.return_value.eq.assert_called_once_with('id', str(call_id))
    call_service.supabase.table.return_value.update.assert_called_once()
    update_args = call_service.supabase.table.return_value.update.call_args[0][0]
    assert update_args['status'] == CallStatus.COMPLETED.value
    assert 'updated_at' in update_args
    call_service.supabase.table.return_value.update.return_value.eq.assert_called_once_with('id', str(call_id))
    assert updated_call.id == str(call_id)
    assert updated_call.status == CallStatus.COMPLETED.value

@pytest.mark.asyncio
async def test_update_call_not_found(call_service):
    call_id = uuid.uuid4()
    update_data = CallUpdate(status=CallStatus.COMPLETED)

    # Mockear la verificación de existencia para no encontrar la llamada
    mock_check_execute = AsyncMock(return_value=MagicMock(data=None))
    call_service.supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute = mock_check_execute

    # Ejecutar y verificar excepción
    with pytest.raises(HTTPException) as exc_info:
        await call_service.update_call(call_id, update_data)
    assert exc_info.value.status_code == 404
    call_service.supabase.table.return_value.update.assert_not_called()

@pytest.mark.asyncio
async def test_delete_call_success(call_service):
    call_id = uuid.uuid4()
    mock_existing_call = {'id': str(call_id)}

    # Mockear la verificación de existencia
    mock_check_execute = AsyncMock(return_value=MagicMock(data=mock_existing_call))
    call_service.supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute = mock_check_execute

    # Mockear la eliminación
    mock_delete_execute = AsyncMock(return_value=MagicMock(data=[mock_existing_call])) # Supabase delete devuelve los datos eliminados
    call_service.supabase.table.return_value.delete.return_value.eq.return_value.execute = mock_delete_execute

    # Ejecutar
    result = await call_service.delete_call(call_id)

    # Verificar
    assert result is True
    call_service.supabase.table.return_value.select.return_value.eq.assert_called_once_with('id', str(call_id))
    call_service.supabase.table.return_value.delete.assert_called_once()
    call_service.supabase.table.return_value.delete.return_value.eq.assert_called_once_with('id', str(call_id))

@pytest.mark.asyncio
async def test_delete_call_not_found(call_service):
    call_id = uuid.uuid4()

    # Mockear la verificación de existencia para no encontrar la llamada
    mock_check_execute = AsyncMock(return_value=MagicMock(data=None))
    call_service.supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute = mock_check_execute

    # Ejecutar y verificar excepción
    with pytest.raises(HTTPException) as exc_info:
        await call_service.delete_call(call_id)
    assert exc_info.value.status_code == 404
    call_service.supabase.table.return_value.delete.assert_not_called()

@pytest.mark.asyncio
async def test_get_call_by_twilio_sid_success(call_service):
    twilio_sid = "ACxxxx1234"
    mock_call_data = {'id': str(uuid.uuid4()), 'twilio_sid': twilio_sid, 'status': 'completed'}

    # Mockear Supabase
    mock_execute = AsyncMock(return_value=MagicMock(data=mock_call_data))
    call_service.supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute = mock_execute

    # Ejecutar
    call = await call_service.get_call_by_twilio_sid(twilio_sid)

    # Verificar
    assert call is not None
    assert call.twilio_sid == twilio_sid
    call_service.supabase.table.return_value.select.return_value.eq.assert_called_once_with('twilio_sid', twilio_sid)

@pytest.mark.asyncio
async def test_get_call_by_twilio_sid_not_found(call_service):
    twilio_sid = "ACxxxx1234"

    # Mockear Supabase para no devolver datos
    mock_execute = AsyncMock(return_value=MagicMock(data=None))
    call_service.supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute = mock_execute

    # Ejecutar
    call = await call_service.get_call_by_twilio_sid(twilio_sid)

    # Verificar
    assert call is None
    call_service.supabase.table.return_value.select.return_value.eq.assert_called_once_with('twilio_sid', twilio_sid)

@pytest.mark.asyncio
async def test_handle_call_response_audio_version_success(call_service):
    call_id = str(uuid.uuid4())
    user_message = "User message"
    ai_response_text = "AI response text"
    generated_audio = b"generated_audio_bytes"
    
    # Mockear dependencias
    mock_call = MagicMock(spec=Call, id=call_id, campaign_id="c1", contact_id="p1", interaction_history=[])
    mock_campaign = MagicMock(name="Campaign Name", objective="Objective")
    mock_contact = MagicMock(name="Contact Name")
    
    call_service.get_call = AsyncMock(return_value=mock_call)
    call_service.campaign_service.get_campaign = AsyncMock(return_value=mock_campaign)
    call_service.contact_service.get_contact = AsyncMock(return_value=mock_contact)
    call_service.ai_service.process_message = AsyncMock(return_value=ai_response_text)
    call_service.elevenlabs_service.generate_audio = AsyncMock(return_value=generated_audio)
    call_service.update_call_history = AsyncMock() # Mockear para no interferir
    
    # Ejecutar
    audio_result = await call_service.handle_call_response(call_id, user_message)
    
    # Verificar
    assert audio_result == generated_audio
    call_service.get_call.assert_called_once_with(call_id)
    call_service.campaign_service.get_campaign.assert_called_once_with("c1")
    call_service.contact_service.get_contact.assert_called_once_with("p1")
    call_service.ai_service.process_message.assert_called_once()
    # Verificar contexto pasado a AI service
    ai_call_args = call_service.ai_service.process_message.call_args[0]
    assert ai_call_args[0] == user_message
    assert ai_call_args[1]["campaign_name"] == mock_campaign.name
    assert ai_call_args[1]["contact_name"] == mock_contact.name
    call_service.elevenlabs_service.generate_audio.assert_called_once_with(ai_response_text)
    call_service.update_call_history.assert_called_once_with(call_id, user_message, ai_response_text)
