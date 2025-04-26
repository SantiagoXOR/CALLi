# tests/routers/test_call_webhook.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from typing import AsyncGenerator, List
import json

from app.main import app
from app.dependencies import get_call_service
from app.services.call_service import CallService, StreamingError

# --- Mock del Generador Asíncrono ---
async def mock_audio_stream_generator(chunks: List[bytes]) -> AsyncGenerator[bytes, None]:
    """Un generador asíncrono simple para usar en los mocks."""
    for chunk in chunks:
        yield chunk
    # Simula que el generador termina

# --- Fixture para el TestClient ---
@pytest.fixture(scope="module")
def client():
    """Crea un TestClient para la aplicación."""
    return TestClient(app)

# --- Tests ---
@pytest.mark.asyncio
async def test_handle_webhook_user_input_success(client: TestClient, mocker: MagicMock):
    """
    Prueba el webhook cuando recibe input del usuario y debe devolver audio.
    """
    # 1. Datos Simulados
    fake_call_sid = "CAxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    fake_user_message = "Hola, quiero información sobre el producto."
    fake_payload = {
        "CallSid": fake_call_sid,
        "SpeechResult": fake_user_message,
        "CallStatus": "in-progress"
        # Añade otros campos que tu webhook pueda esperar
    }
    expected_audio_chunks = [b"audio_chunk_1_", b"audio_chunk_2_", b"audio_chunk_3"]
    expected_concatenated_audio = b"".join(expected_audio_chunks)

    # 2. Mockear CallService.handle_call_response
    # Crea un mock para la instancia de CallService
    mock_call_service_instance = mocker.MagicMock(spec=CallService)
    # Configura el método mockeado para que devuelva nuestro generador falso
    mock_call_service_instance.handle_call_response = AsyncMock(
        return_value=mock_audio_stream_generator(expected_audio_chunks)
    )
    # Configura el método handle_call_end por si acaso (no debería llamarse aquí)
    mock_call_service_instance.handle_call_end = AsyncMock()

    # 3. Sobrescribir la dependencia: Haz que get_call_service devuelva nuestro mock
    # Esto asegura que cuando el router pida CallService, reciba nuestro mock
    app.dependency_overrides[get_call_service] = lambda: mock_call_service_instance

    # 4. Enviar Solicitud POST al Webhook
    response = client.post(
        "/api/v1/calls/webhook", # Asegúrate que esta ruta sea correcta
        json=fake_payload # Envía el payload como JSON
        # O usa 'data=fake_payload' si esperas form-data y ajusta el parsing en el webhook
    )

    # 5. Verificar Respuesta HTTP
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg" # O el media type correcto
    # Iterar sobre la respuesta de streaming para verificar el contenido
    received_content = b""
    for chunk in response.iter_bytes():
        received_content += chunk
    assert received_content == expected_concatenated_audio

    # 6. Verificar Llamada al Servicio Mockeado
    mock_call_service_instance.handle_call_response.assert_awaited_once_with(
        call_id=fake_call_sid,
        user_message=fake_user_message
    )
    # Asegurarse de que handle_call_end NO fue llamado
    mock_call_service_instance.handle_call_end.assert_not_awaited()

    # Limpiar la sobrescritura de dependencia después del test
    app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_handle_webhook_call_ended(client: TestClient, mocker: MagicMock):
    """
    Prueba el webhook cuando recibe un evento de finalización de llamada.
    """
    # 1. Datos Simulados
    fake_call_sid = "CAyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
    final_status = "completed"
    fake_payload = {
        "CallSid": fake_call_sid,
        "CallStatus": final_status
    }

    # 2. Mockear CallService
    mock_call_service_instance = mocker.MagicMock(spec=CallService)
    mock_call_service_instance.handle_call_end = AsyncMock() # Solo necesitamos mockear end
    mock_call_service_instance.handle_call_response = AsyncMock() # No debería llamarse

    # 3. Sobrescribir Dependencia
    app.dependency_overrides[get_call_service] = lambda: mock_call_service_instance

    # 4. Enviar Solicitud POST
    response = client.post("/api/v1/calls/webhook", json=fake_payload)

    # 5. Verificar Respuesta HTTP
    assert response.status_code == 200
    assert response.content == b"" # Esperamos cuerpo vacío

    # 6. Verificar Llamada al Servicio Mockeado
    mock_call_service_instance.handle_call_end.assert_awaited_once_with(
        call_id=fake_call_sid # Corregido: Solo espera call_id
    )
    mock_call_service_instance.handle_call_response.assert_not_awaited()

    # Limpiar la sobrescritura
    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_handle_webhook_streaming_error(client: TestClient, mocker: MagicMock):
    """Prueba el manejo de StreamingError durante la generación de audio."""
    fake_call_sid = "CAzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
    fake_user_message = "Mensaje que causará error"
    fake_payload = {
        "CallSid": fake_call_sid,
        "SpeechResult": fake_user_message,
        "CallStatus": "in-progress"
    }

    mock_call_service_instance = mocker.MagicMock(spec=CallService)
    mock_call_service_instance.handle_call_response = AsyncMock(
        side_effect=StreamingError("Error durante streaming")
    )

    app.dependency_overrides[get_call_service] = lambda: mock_call_service_instance

    response = client.post("/api/v1/calls/webhook", json=fake_payload)

    assert response.status_code == 500
    assert response.content == b""
    mock_call_service_instance.handle_call_response.assert_awaited_once_with(
        call_id=fake_call_sid,
        user_message=fake_user_message
    )

    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_handle_webhook_form_data(client: TestClient, mocker: MagicMock):
    """Prueba el manejo de payload en formato form-data."""
    fake_call_sid = "CAwwwwwwwwwwwwwwwwwwwwwwwwww"
    fake_user_message = "Mensaje via form-data"
    fake_payload = {
        "CallSid": fake_call_sid,
        "SpeechResult": fake_user_message,
        "CallStatus": "in-progress"
    }

    expected_audio_chunks = [b"audio_chunk_form_data"]
    mock_call_service_instance = mocker.MagicMock(spec=CallService)
    mock_call_service_instance.handle_call_response = AsyncMock(
        return_value=mock_audio_stream_generator(expected_audio_chunks)
    )

    app.dependency_overrides[get_call_service] = lambda: mock_call_service_instance

    response = client.post(
        "/api/v1/calls/webhook",
        data=fake_payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
    # Iterar sobre la respuesta de streaming para verificar el contenido
    received_content = b""
    for chunk in response.iter_bytes():
        received_content += chunk
    assert received_content == b"audio_chunk_form_data"

    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_handle_webhook_intermediate_event(client: TestClient, mocker: MagicMock):
    """Prueba el manejo de eventos intermedios sin input de usuario."""
    fake_call_sid = "CAvvvvvvvvvvvvvvvvvvvvvvvvvv"
    fake_payload = {
        "CallSid": fake_call_sid,
        "CallStatus": "ringing"
    }

    mock_call_service_instance = mocker.MagicMock(spec=CallService)
    app.dependency_overrides[get_call_service] = lambda: mock_call_service_instance

    response = client.post("/api/v1/calls/webhook", json=fake_payload)

    assert response.status_code == 200
    assert response.content == b""
    mock_call_service_instance.handle_call_response.assert_not_called()
    mock_call_service_instance.handle_call_end.assert_not_called()

    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_handle_webhook_invalid_json(client: TestClient, mocker: MagicMock):
    """Prueba el manejo de JSON inválido en el payload."""
    invalid_json = "{"

    mock_call_service_instance = mocker.MagicMock(spec=CallService)
    app.dependency_overrides[get_call_service] = lambda: mock_call_service_instance

    response = client.post(
        "/api/v1/calls/webhook",
        data=invalid_json,
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422
    mock_call_service_instance.handle_call_response.assert_not_called()
    mock_call_service_instance.handle_call_end.assert_not_called()

    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_handle_webhook_metadata_parsing(client: TestClient, mocker: MagicMock):
    """Prueba el manejo de metadata en formato JSON string."""
    fake_call_sid = "CAuuuuuuuuuuuuuuuuuuuuuuuuuu"
    fake_metadata = json.dumps({"conversation_tracking_id": "track-123"})
    fake_payload = {
        "CallSid": fake_call_sid,
        "metadata": fake_metadata,
        "CallStatus": "in-progress",
        "SpeechResult": "Hola"
    }

    expected_audio_chunks = [b"audio_response"]
    mock_call_service_instance = mocker.MagicMock(spec=CallService)
    mock_call_service_instance.handle_call_response = AsyncMock(
        return_value=mock_audio_stream_generator(expected_audio_chunks)
    )

    app.dependency_overrides[get_call_service] = lambda: mock_call_service_instance

    response = client.post("/api/v1/calls/webhook", json=fake_payload)

    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
    # Iterar sobre la respuesta de streaming para verificar el contenido
    received_content = b""
    for chunk in response.iter_bytes():
        received_content += chunk
    assert received_content == b"audio_response"

    app.dependency_overrides = {}
