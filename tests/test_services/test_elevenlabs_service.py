import pytest
from unittest.mock import patch, MagicMock
from app.services.elevenlabs_service import ElevenLabsService

@pytest.fixture
def elevenlabs_service():
    service = ElevenLabsService()
    yield service

@pytest.mark.asyncio
async def test_generate_audio(elevenlabs_service):
    """Prueba la generación de audio."""
    test_text = "Texto de prueba"
    test_voice = "Bella"
    
    with patch('app.services.elevenlabs_service.generate') as mock_generate:
        mock_generate.return_value = b"audio_data"
        audio = await elevenlabs_service.generate_audio(test_text, test_voice)
        
        assert audio == b"audio_data"
        mock_generate.assert_called_once_with(text=test_text, voice=test_voice)

@pytest.mark.asyncio
async def test_start_conversation(elevenlabs_service):
    """Prueba el inicio de una conversación."""
    test_voice = "Bella"
    
    await elevenlabs_service.start_conversation(test_voice)
    
    assert elevenlabs_service.conversation is not None
    assert isinstance(elevenlabs_service.conversation, MagicMock)

@pytest.mark.asyncio
async def test_generate_response(elevenlabs_service):
    """Prueba la generación de respuesta en una conversación."""
    test_text = "Hola mundo"
    
    # Primero probamos sin conversación iniciada
    response = await elevenlabs_service.generate_response(test_text)
    assert response is not None
    
    # Luego probamos con conversación ya iniciada
    await elevenlabs_service.start_conversation()
    response = await elevenlabs_service.generate_response(test_text)
    assert response is not None

@pytest.mark.asyncio
async def test_error_handling(elevenlabs_service):
    """Prueba el manejo de errores."""
    with patch('app.services.elevenlabs_service.generate', 
               side_effect=Exception("API Error")):
        with pytest.raises(Exception) as exc_info:
            await elevenlabs_service.generate_audio("test")
        assert "API Error" in str(exc_info.value)
