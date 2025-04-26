import pytest
from app.config.redis_client import (
    generate_conversation_cache_key,
    set_in_cache,
    get_from_cache
)

@pytest.mark.asyncio
class TestRedisClient:
    async def test_generate_cache_key(self):
        """Prueba la generación de claves de caché."""
        conv_id = "test-123"
        key = generate_conversation_cache_key(conv_id)
        assert key == f"conv:{conv_id}"
        assert isinstance(key, str)

    async def test_cache_operations(self):
        """Prueba operaciones básicas de caché."""
        test_key = "test-key"
        test_data = {"message": "test", "timestamp": "2023-01-01"}
        
        # Guardar en caché
        await set_in_cache(test_key, test_data, expire=60)
        
        # Recuperar de caché
        cached_data = await get_from_cache(test_key)
        assert cached_data == test_data
        
        # Verificar expiración
        import asyncio
        await asyncio.sleep(61)
        expired_data = await get_from_cache(test_key)
        assert expired_data is None

    async def test_invalid_cache_key(self):
        """Prueba el manejo de claves inválidas."""
        invalid_data = await get_from_cache("nonexistent-key")
        assert invalid_data is None
