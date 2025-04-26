from redis import Redis
from typing import Any, Dict, List, Optional
import json
import logging
from app.models.cache_metrics import CacheMetrics

# Configurar cliente Redis para conectarse al contenedor de Redis
redis_client = Redis(host='redis', port=6379, db=0)
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
        redis_client.setex(
            key,
            expire,
            json.dumps(value)
        )
        return True
    except Exception as e:
        logger.error(f"Error al guardar en caché: {str(e)}")
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
        return json.loads(value) if value else None
    except Exception as e:
        logger.error(f"Error al recuperar de caché: {str(e)}")
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
        logger.error(f"Error al eliminar de caché: {str(e)}")
        return False

async def get_cache_metrics() -> CacheMetrics:
    """Obtiene métricas de la caché.

    Returns:
        CacheMetrics: Objeto con las métricas de caché
    """
    try:
        info = redis_client.info()
        return CacheMetrics(
            total_keys=info.get('db0', {}).get('keys', 0),
            memory_used=info.get('used_memory_human', '0'),
            hit_rate=info.get('keyspace_hits', 0) / (info.get('keyspace_hits', 0) + info.get('keyspace_misses', 1) or 1),
            uptime=info.get('uptime_in_seconds', 0)
        )
    except Exception as e:
        logger.error(f"Error al obtener métricas de caché: {str(e)}")
        return CacheMetrics(
            total_keys=0,
            memory_used="0",
            hit_rate=0.0,
            uptime=0
        )

async def sync_to_supabase(table_name: str, key_prefix: Optional[str] = None) -> bool:
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
            for key in redis_client.scan_iter(f"{key_prefix}*"):
                keys.append(key.decode('utf-8'))
        else:
            for key in redis_client.scan_iter():
                keys.append(key.decode('utf-8'))

        # Sincronizar cada clave
        for key in keys:
            value = await get_from_cache(key)
            if value:
                # Extraer ID de la clave (asumiendo formato "prefix:id")
                if ':' in key:
                    entity_id = key.split(':', 1)[1]
                else:
                    entity_id = key

                # Upsert a Supabase
                supabase_client.table(table_name).upsert({
                    "id": entity_id,
                    "data": value,
                    "updated_at": "now()"
                }).execute()

        return True
    except Exception as e:
        logger.error(f"Error al sincronizar con Supabase: {str(e)}")
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
        logger.error(f"Error al limpiar caché: {str(e)}")
        return False
