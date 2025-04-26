import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime
from app.services.ai_conversation_service import AIConversationService

@pytest.fixture
async def mock_llm():
    mock = AsyncMock()
    mock.predict.return_value = "Respuesta de prueba"
    return mock

@pytest.fixture
async def mock_redis():
    mock = AsyncMock()
    mock.get.return_value = None
    mock.setex.return_value = True
    return mock

@pytest.fixture
async def ai_service(mock_llm, mock_redis):
    service = AIConversationService(
        model_name="gpt-4",
        redis_client=mock_redis
    )
    service.llm = mock_llm
    return service

class TestAIConversationService:
    @pytest.mark.asyncio
    async def test_process_message_basic(self, ai_service):
        """Prueba el procesamiento básico de un mensaje."""
        response = await ai_service.process_message(
            message="Hola, necesito información",
            conversation_id="test-123"
        )
        
        assert isinstance(response, dict)
        assert "response" in response
        assert "input_sentiment" in response
        assert "conversation_id" in response
        assert response["conversation_id"] == "test-123"

    @pytest.mark.asyncio
    async def test_sentiment_analysis(self, ai_service):
        """Prueba el análisis de sentimientos."""
        test_messages = [
            ("¡Excelente servicio!", "positive"),
            ("Esto es terrible", "negative"),
            ("OK, entiendo", "neutral")
        ]
        
        for message, expected_sentiment in test_messages:
            sentiment = await ai_service.analyze_sentiment(message)
            assert "primary_emotion" in sentiment
            assert "score" in sentiment
            assert isinstance(sentiment["score"], float)
            assert 0 <= sentiment["score"] <= 1

    @pytest.mark.asyncio
    async def test_error_handling(self, ai_service, mock_llm):
        """Prueba el manejo de errores."""
        mock_llm.predict.side_effect = Exception("Error de API")
        
        with pytest.raises(Exception) as exc_info:
            await ai_service.process_message("test message")
        
        assert "Error procesando mensaje" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_conversation_caching(self, ai_service, mock_redis):
        """Prueba el sistema de caché de conversaciones."""
        conv_id = "cache-test-123"
        test_message = "mensaje de prueba"
        
        # Primera llamada - debe intentar obtener del caché
        await ai_service.process_message(
            message=test_message,
            conversation_id=conv_id
        )
        
        mock_redis.get.assert_called_once()
        mock_redis.setex.assert_called_once()

    @pytest.mark.asyncio
    async def test_context_handling(self, ai_service):
        """Prueba el manejo de contexto adicional."""
        context = {
            "campaign_id": "camp-123",
            "user_preferences": {"language": "es"}
        }
        
        response = await ai_service.process_message(
            message="Hola",
            conversation_id="test-123",
            context=context
        )
        
        assert response["context"] == context
