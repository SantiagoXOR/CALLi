import pytest
import respx
from httpx import Response, AsyncClient
from app.services.elevenlabs_service import ElevenLabsService, ElevenLabsAPIError
from app.config.settings import settings
from typing import Dict, Any, Optional

@pytest.fixture
async def elevenlabs_service():
    service = ElevenLabsService()
    service.api_key = "test_api_key"
    return service

@pytest.mark.asyncio
class TestElevenLabsService:
    async def test_initiate_outbound_call_success(self, elevenlabs_service):
        """Verifica que la llamada saliente se inicia correctamente"""
        expected_payload = {
            "to_number": "+1234567890",
            "voice_id": "default_voice",
            "model_id": settings.ELEVENLABS_MODEL_ID,
            "twilio_account_sid": settings.TWILIO_ACCOUNT_SID,
            "twilio_auth_token": settings.TWILIO_AUTH_TOKEN,
            "from_number": settings.TWILIO_FROM_NUMBER,
            "webhook_url": f"{settings.APP_BASE_URL}/api/v1/calls/webhook",
            "metadata": {"call_id": "test-call-123"}
        }

        with respx.mock(assert_all_mocked=True) as mock:
            mock.post(
                "https://api.elevenlabs.io/v1/conversations/twilio/outbound-call"
            ).mock(
                return_value=Response(200, json={"call_id": "test-call-123"})
            )

            response = await elevenlabs_service.initiate_outbound_call(
                to_number="+1234567890",
                metadata={"call_id": "test-call-123"}
            )

            assert response["call_id"] == "test-call-123"
            assert mock.calls.last.request.headers["xi-api-key"] == "test_api_key"
            assert mock.calls.last.request.headers["Content-Type"] == "application/json"
            assert mock.calls.last.request.json() == expected_payload

    async def test_initiate_outbound_call_error(self, elevenlabs_service):
        """Verifica el manejo correcto de errores de la API"""
        with respx.mock(assert_all_mocked=True) as mock:
            mock.post(
                "https://api.elevenlabs.io/v1/conversations/twilio/outbound-call"
            ).mock(
                return_value=Response(400, json={"error": "Invalid request"})
            )

            with pytest.raises(ElevenLabsAPIError) as exc_info:
                await elevenlabs_service.initiate_outbound_call(
                    to_number="+1234567890",
                    metadata={"call_id": "test-call-123"}
                )

            assert "Invalid request" in str(exc_info.value)

    async def test_initiate_outbound_call_with_prompt(self, elevenlabs_service):
        """Verifica que el prompt opcional se incluye correctamente"""
        prompt = "Bienvenido a nuestra llamada de prueba"
        
        with respx.mock(assert_all_mocked=True) as mock:
            mock.post(
                "https://api.elevenlabs.io/v1/conversations/twilio/outbound-call"
            ).mock(
                return_value=Response(200, json={"call_id": "test-call-123"})
            )

            await elevenlabs_service.initiate_outbound_call(
                to_number="+1234567890",
                prompt=prompt,
                metadata={"call_id": "test-call-123"}
            )

            assert mock.calls.last.request.json()["prompt"] == prompt

    async def test_generate_audio_success(self, elevenlabs_service):
        """Verifica generación de audio exitosa"""
        with patch("app.services.elevenlabs_service.generate") as mock_generate:
            mock_generate.return_value = b"audio_data"
            with patch('app.services.elevenlabs_service.secrets_manager.get_elevenlabs_credentials', 
                     new_callable=AsyncMock, return_value={"api_key": "mock_api_key"}):
                audio = await elevenlabs_service.generate_audio("Test", "Bella")
                assert audio == b"audio_data"

    async def test_generate_audio_failure(self, elevenlabs_service):
        """Verifica manejo de errores en generación de audio"""
        with patch("app.services.elevenlabs_service.generate") as mock_generate:
            mock_generate.side_effect = Exception("API Error")
            with patch('app.services.elevenlabs_service.secrets_manager.get_elevenlabs_credentials', 
                     new_callable=AsyncMock, return_value={"api_key": "mock_api_key"}):
                with pytest.raises(ElevenLabsAPIError):
                    await elevenlabs_service.generate_audio("Test", "Bella")
