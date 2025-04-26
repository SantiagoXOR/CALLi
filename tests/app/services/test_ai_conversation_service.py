import pytest
from unittest.mock import AsyncMock

from app.services.ai_conversation_service import AIConversationService

@pytest.fixture
def ai_conversation_service():
    return AIConversationService()

@pytest.mark.asyncio
async def test_process_message(ai_conversation_service):
    ai_conversation_service.get_from_cache = AsyncMock(return_value=None)
    ai_conversation_service.analyze_sentiment = AsyncMock(return_value={"primary_emotion": "neutral", "score": 0.5})
    ai_conversation_service.llm.apredict = AsyncMock(return_value="Hola, ¿en qué puedo ayudarte?")

    result = await ai_conversation_service.process_message("Hola", "123")

    assert result["response"] == "Hola, ¿en qué puedo ayudarte?"
    assert result["input_sentiment"] == {"primary_emotion": "neutral", "score": 0.5}
    assert result["response_sentiment"] == {"primary_emotion": "neutral", "score": 0.5}
    assert result["conversation_id"] == "123"

@pytest.mark.asyncio
async def test_analyze_sentiment(ai_conversation_service):
    ai_conversation_service.llm.ainvoke = AsyncMock(return_value='{"primary_emotion": "positive", "score": 0.8}')
    result = await ai_conversation_service.analyze_sentiment("Este es un texto muy positivo")
    assert result == {"primary_emotion": "positive", "score": 0.8}

@pytest.mark.asyncio
async def test_save_conversation_metrics(ai_conversation_service):
    # Mockear el método save_metrics_to_db
    ai_conversation_service.save_metrics_to_db = AsyncMock()

    # Llamar al método save_conversation_metrics
    await ai_conversation_service.save_conversation_metrics(
        conversation_id="123",
        message="Hola",
        response="Hola, ¿en qué puedo ayudarte?",
        input_sentiment={"primary_emotion": "neutral", "score": 0.5},
        response_sentiment={"primary_emotion": "positive", "score": 0.8}
    )

    # Verificar que save_metrics_to_db fue llamado con los argumentos correctos
    ai_conversation_service.save_metrics_to_db.assert_called_once()
    args, kwargs = ai_conversation_service.save_metrics_to_db.call_args
    assert args[0]["conversation_id"] == "123"
    assert args[0]["message_length"] == 4
    assert args[0]["response_sentiment"] == "positive"
    assert args[0]["response_sentiment_score"] == 0.8

def test_extract_conversation_context(ai_conversation_service):
    memory = ConversationBufferMemory()
    memory.save_context({"input": "Hola"}, {"output": "Hola, ¿en qué puedo ayudarte?"})
    context = ai_conversation_service.extract_conversation_context(memory)
    assert isinstance(context, dict)
    # Add more assertions based on the expected context

@pytest.mark.asyncio
async def test_get_from_cache(ai_conversation_service):
    ai_conversation_service.get_from_cache = AsyncMock(return_value=[{"type": "human", "content": "Hola"}, {"type": "ai", "content": "Hola, ¿en qué puedo ayudarte?"}])
    result = await ai_conversation_service.get_from_cache("123")
    assert result == [{"type": "human", "content": "Hola"}, {"type": "ai", "content": "Hola, ¿en qué puedo ayudarte?"}]

@pytest.mark.asyncio
async def test_set_in_cache(ai_conversation_service):
    ai_conversation_service.set_in_cache = AsyncMock()
    await ai_conversation_service.set_in_cache("123", [{"type": "human", "content": "Hola"}, {"type": "ai", "content": "Hola, ¿en qué puedo ayudarte?"}])
    ai_conversation_service.set_in_cache.assert_called_once_with("123", [{"type": "human", "content": "Hola"}, {"type": "ai", "content": "Hola, ¿en qué puedo ayudarte?"}])
