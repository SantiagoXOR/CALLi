import json
import logging
from typing import Any

from redis import Redis

from app.models.cache_metrics import CacheMetrics

# Configurar cliente Redis para conectarse al contenedor de Redis
redis_client = Redis(host="redis", port=6379, db=0)
logger = logging.getLogger(__name__)


def generate_conversation_cache_key(conversation_id: str) -> str:
    """Genera una clave para la caché de conversaciones."""
    return f"conv:{conversation_id}"


async def set_in_cache(key: str, value: Any, expire: int = 3600) -> bool:
    """Guarda valor en caché con expiración.

    Args:
        key: Clave para almacenar el valor
        value: Valor a almacenar
        expire: Tiempo de expiración en segundos

    Returns:
        bool: True si se guardó correctamente, False en caso contrario
    """
    try:
        redis_client.setex(key, expire, json.dumps(value))
        return True
    except Exception as e:
        logger.error(f"Error al guardar en caché: {e!s}")
        return False


async def get_from_cache(key: str) -> Any:
    """Recupera valor de caché.

    Args:
        key: Clave a recuperar

    Returns:
        Any: Valor recuperado o None si no existe
    """
    try:
        value = redis_client.get(key)
        if value:
            # Decodificar bytes a string si es necesario
            value_str = value.decode("utf-8") if isinstance(value, bytes) else value
            return json.loads(value_str)
        return None
    except Exception as e:
        logger.error(f"Error al recuperar de caché: {e!s}")
        return None


async def delete_from_cache(key: str) -> bool:
    """Elimina un valor de la caché.

    Args:
        key: Clave a eliminar

    Returns:
        bool: True si se eliminó correctamente, False en caso contrario
    """
    try:
        return bool(redis_client.delete(key))
    except Exception as e:
        logger.error(f"Error al eliminar de caché: {e!s}")
        return False


async def get_cache_metrics() -> CacheMetrics:
    """Obtiene métricas de la caché.

    Returns:
        CacheMetrics: Objeto con las métricas de caché
    """
    try:
        info = redis_client.info()
        return CacheMetrics(
            total_keys=info.get("db0", {}).get("keys", 0),
            memory_used=info.get("used_memory_human", "0"),
            hit_rate=info.get("keyspace_hits", 0)
            / (info.get("keyspace_hits", 0) + info.get("keyspace_misses", 1) or 1),
            uptime=info.get("uptime_in_seconds", 0),
        )
    except Exception as e:
        logger.error(f"Error al obtener métricas de caché: {e!s}")
        return CacheMetrics(total_keys=0, memory_used="0", hit_rate=0.0, uptime=0)


async def sync_to_supabase(table_name: str, key_prefix: str | None = None) -> bool:
    """Sincroniza datos de la caché a Supabase.

    Args:
        table_name: Nombre de la tabla en Supabase
        key_prefix: Prefijo de claves a sincronizar (opcional)

    Returns:
        bool: True si se sincronizó correctamente, False en caso contrario
    """
    try:
        from app.config.supabase import supabase_client

        # Obtener todas las claves que coincidan con el prefijo
        keys = []
        if key_prefix:
            for key_bytes in redis_client.scan_iter(f"{key_prefix}*"):
                # Asegurar que key sea str para operaciones posteriores
                key_str = key_bytes.decode("utf-8") if isinstance(key_bytes, bytes) else key_bytes
                keys.append(key_str)
        else:
            for key_bytes in redis_client.scan_iter():
                # Asegurar que key sea str para operaciones posteriores
                key_str = key_bytes.decode("utf-8") if isinstance(key_bytes, bytes) else key_bytes
                keys.append(key_str)

        # Sincronizar cada clave
        for key in keys:
            value = await get_from_cache(key)
            if value:
                # Extraer ID de la clave (asumiendo formato "prefix:id")
                if ":" in key:
                    entity_id = key.split(":", 1)[1]
                else:
                    entity_id = key

                # Upsert a Supabase
                supabase_client.table(table_name).upsert(
                    {"id": entity_id, "data": value, "updated_at": "now()"}
                ).execute()

        return True
    except Exception as e:
        logger.error(f"Error al sincronizar con Supabase: {e!s}")
        return False


async def clear_cache() -> bool:
    """Limpia toda la caché.

    Returns:
        bool: True si se limpió correctamente, False en caso contrario
    """
    try:
        redis_client.flushdb()
        return True
    except Exception as e:
        logger.error(f"Error al limpiar caché: {e!s}")
        return False
