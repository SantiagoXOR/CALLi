from unittest.mock import AsyncMock

import pytest

from isolated_ai_redis_tests import (
    AIConversationService,
    generate_conversation_cache_key,
)


class TestAIRedisIntegration:
    @pytest.mark.asyncio
    async def test_conversation_flow(self):
        # Configurar mocks
        redis_mock = AsyncMock()
        redis_mock.get.return_value = None
        redis_mock.setex.return_value = True

        # Configurar servicio con mock de Redis
        service = AIConversationService()
        service.redis_client = redis_mock

        # Simular conversación
        conv_id = "test-integration-123"
        messages = ["Hola", "¿Cómo estás?", "Necesito ayuda"]

        for msg in messages:
            response = await service.process_message(message=msg, conversation_id=conv_id)

            # Verificar interacción con Redis
            cache_key = generate_conversation_cache_key(conv_id)
            redis_mock.get.assert_called_with(cache_key)
            redis_mock.setex.assert_called()

            # Verificar respuesta
            assert response["conversation_id"] == conv_id
            assert "response" in response
            assert "input_sentiment" in response

    @pytest.mark.asyncio
    async def test_cached_conversation(self):
        # Configurar mock con caché existente
        redis_mock = AsyncMock()
        cached_data = {"history": ["Mensaje previo"], "context": {"user": "test"}}
        redis_mock.get.return_value = cached_data

        service = AIConversationService()
        service.redis_client = redis_mock

        response = await service.process_message("Nuevo mensaje", conversation_id="cached-conv")

        # Verificar que usó el caché
        redis_mock.get.assert_called()
        assert "context" in response


import asyncio
import time

from app.utils.logger import get_logger  # Assuming logger is configured

logger = get_logger(__name__)


class TestAIRedisLoadTesting:
    @pytest.mark.asyncio
    async def test_concurrent_load(self):
        """Prueba de carga con múltiples conversaciones simultáneas."""
        redis_mock = AsyncMock()
        redis_mock.get.return_value = None  # Simulate cache miss
        redis_mock.setex.return_value = True

        service = AIConversationService()
        service.redis_client = redis_mock

        # Simular 50 conversaciones simultáneas
        num_conversations = 50
        messages_per_conv = 5

        async def conversation_simulation(conv_id):
            for i in range(messages_per_conv):
                response = await service.process_message(
                    f"Message {i}", conversation_id=f"load-test-{conv_id}"
                )
                assert response is not None

        tasks = [conversation_simulation(i) for i in range(num_conversations)]

        start_time = time.time()
        await asyncio.gather(*tasks)
        end_time = time.time()

        total_requests = num_conversations * messages_per_conv
        duration = end_time - start_time
        requests_per_second = total_requests / duration

        logger.info(f"Load test completed: {requests_per_second:.2f} req/s")
        assert requests_per_second > 10  # Mínimo 10 req/s


if __name__ == "__main__":
    pytest.main(["-v", __file__])
