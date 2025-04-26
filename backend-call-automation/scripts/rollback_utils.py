"""Utils para operaciones de rollback de la integración con ElevenLabs."""

import logging
import os
import asyncio
import json
from typing import List, Optional, Dict, Tuple
from pathlib import Path
from contextlib import asynccontextmanager

# Módulos internos y librerías externas
from app.config.redis_client import redis_client
from app.config.settings import settings, get_settings
from app.utils.connection_pool import ConnectionPool
from prometheus_client import REGISTRY

logger = logging.getLogger(__name__)

# Configuración de snapshots para rollback
SNAPSHOT_DIR = Path(__file__).parent / "snapshots"
SNAPSHOT_FILE = SNAPSHOT_DIR / "elevenlabs_config_snapshot.json"

async def take_config_snapshot() -> None:
    """Guarda una instantánea de la configuración actual para posibles rollbacks."""
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    snapshot = {
        "env_vars": {
            k: v for k, v in os.environ.items()
            if k.startswith("ELEVENLABS_")
        },
        "settings": {
            "ELEVENLABS_MAX_RETRIES": getattr(settings, "ELEVENLABS_MAX_RETRIES", None),
            "ELEVENLABS_CONNECTION_TIMEOUT": getattr(settings, "ELEVENLABS_CONNECTION_TIMEOUT", None),
            "ELEVENLABS_POOL_SIZE": getattr(settings, "ELEVENLABS_POL_SIZE", None)
        }
    }

    try:
        with open(SNAPSHOT_FILE, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)
        logger.info(f"Snapshot de configuración guardado en {SNAPSHOT_FILE}")
    except TypeError as e:
        logger.error(f"Error de serialización al guardar snapshot: {e}")
        raise
    except Exception as e:
        logger.error(f"Error al guardar snapshot de configuración: {e}")
        raise

async def clear_redis_cache(pattern: str = "elevenlabs:*") -> int:
    """Limpia claves Redis usando SCAN para evitar bloqueos. Detecta cliente sync/async."""
    deleted_count = 0
    try:
        is_async = hasattr(redis_client, 'scan_iter') and asyncio.iscoroutinefunction(redis_client.delete)

        if is_async:
            async for key in redis_client.scan_iter(match=pattern, count=100):
                await redis_client.delete(key)
                deleted_count += 1
        else:
             for key in redis_client.scan_iter(match=pattern, count=100):
                 redis_client.delete(key)
                 deleted_count += 1

        if deleted_count > 0:
            logger.info(f"Eliminadas {deleted_count} claves Redis con patrón '{pattern}' usando SCAN")
        else:
            logger.info(f"No se encontraron claves Redis con patrón '{pattern}'")
        return deleted_count
    except AttributeError:
         logger.error("Error: El cliente Redis no parece tener el método 'scan_iter' o 'delete'")
         raise
    except Exception as e:
        logger.error(f"Error al limpiar caché Redis: {e}")
        raise

async def reset_prometheus_metrics(
    metric_names: Optional[List[str]] = None
) -> Dict[str, Tuple[bool, Optional[str]]]:
    """
    Resetea métricas Prometheus específicas DESREGISTRÁNDOLAS.
    Retorna un dict con el estado de cada métrica procesada.

    Args:
        metric_names: Lista de métricas a resetear. Si None, usa las defaults.

    Returns:
        Dict[str, Tuple[bool, str]]:
            - Clave: nombre de métrica
            - Valor: (success: bool, message: str)
    """
    default_metrics = [
        'elevenlabs_requests_total',
        'elevenlabs_errors_total',
        'elevenlabs_request_duration_seconds',
        'elevenlabs_generation_duration_seconds',
        'elevenlabs_pool_connections_active',
        'elevenlabs_pool_usage_ratio',
        'elevenlabs_audio_quality_score',
        'elevenlabs_retry_count_total'
    ]

    metrics_to_reset = metric_names or default_metrics
    results = {}

    logger.info(f"Intentando resetear (desregistrar) métricas Prometheus: {metrics_to_reset}")

    for metric_name in metrics_to_reset:
        try:
            if metric_name in REGISTRY._names_to_collectors:
                collector = REGISTRY._names_to_collectors[metric_name]
                REGISTRY.unregister(collector)
                results[metric_name] = (True, f"Métrica {metric_name} desregistrada")
                logger.info(f"Métrica {metric_name} desregistrada exitosamente")
            else:
                results[metric_name] = (False, f"Métrica {metric_name} no encontrada")
                logger.warning(f"Métrica {metric_name} no encontrada en el registro")
        except Exception as e:
            results[metric_name] = (False, f"Error al desregistrar {metric_name}: {str(e)}")
            logger.error(f"Error al desregistrar métrica {metric_name}", exc_info=True)

    return results

async def close_all_elevenlabs_connections() -> None:
    """Cierra conexiones activas del pool de conexiones, priorizando 'close_all'."""
    closed_count = 0
    try:
        pool = ConnectionPool.get_instance()

        if hasattr(pool, 'close_all') and callable(pool.close_all):
            if asyncio.iscoroutinefunction(pool.close_all):
                result = await pool.close_all()
            else:
                result = pool.close_all()
            closed_count = result if isinstance(result, int) else -1
            logger.info(f"Método pool.close_all() ejecutado. Conexiones cerradas: {'desconocido' if closed_count == -1 else closed_count}")

        elif hasattr(pool, 'get_active_connections') and callable(pool.get_active_connections) and \
             hasattr(pool, 'terminate_connection') and callable(pool.terminate_connection):

            logger.info("Usando fallback: get_active_connections y terminate_connection")
            get_is_async = asyncio.iscoroutinefunction(pool.get_active_connections)
            term_is_async = asyncio.iscoroutinefunction(pool.terminate_connection)

            connections = await pool.get_active_connections() if get_is_async else pool.get_active_connections()

            if connections:
                logger.info(f"Intentando terminar {len(connections)} conexiones activas individualmente...")
                for conn in connections:
                    try:
                        if term_is_async:
                            await pool.terminate_connection(conn)
                        else:
                            pool.terminate_connection(conn)
                        closed_count += 1
                    except Exception as term_e:
                        logger.error(f"Error al terminar conexión individual ({conn}): {term_e}")
                logger.info(f"Terminadas {closed_count} conexiones individualmente.")
            else:
                logger.info("No se encontraron conexiones activas para terminar.")
        else:
            logger.warning("El pool de conexiones no expone métodos para cerrar conexiones explícitamente.")
    except Exception as e:
        logger.error(f"Error al intentar cerrar conexiones de ElevenLabs: {e}")
        raise

async def restore_previous_config() -> None:
    """Restaura configuración desde snapshot si existe, sino usa defaults."""
    try:
        config_source = "desconocida"
        if SNAPSHOT_FILE.exists() and SNAPSHOT_FILE.is_file():
            logger.info(f"Intentando restaurar configuración desde snapshot: {SNAPSHOT_FILE}")
            try:
                with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:
                    snapshot = json.load(f)
                config_source = f"snapshot ({SNAPSHOT_FILE.name})"

                env_vars_to_restore = snapshot.get('env_vars', {})
                logger.info(f"Restaurando {len(env_vars_to_restore)} variables de entorno desde snapshot...")
                for k, v in env_vars_to_restore.items():
                    if k.startswith("ELEVENLABS_"):
                         os.environ[k] = str(v) if v is not None else ""

                settings_to_restore = snapshot.get('settings', {})
                logger.info(f"Restaurando {len(settings_to_restore)} atributos de settings desde snapshot...")
                for k, v in settings_to_restore.items():
                     if hasattr(settings, k):
                         setattr(settings, k, v)
                     else:
                         logger.warning(f"El atributo '{k}' del snapshot no existe en el objeto settings actual.")

            except json.JSONDecodeError as json_e:
                logger.error(f"Error al decodificar snapshot JSON ({SNAPSHOT_FILE}): {json_e}. Se usará configuración por defecto.")
                config_source = "defaults (error snapshot)"
                await _apply_default_config()
            except Exception as snap_e:
                 logger.error(f"Error inesperado al procesar snapshot ({SNAPSHOT_FILE}): {snap_e}. Se usará configuración por defecto.")
                 config_source = "defaults (error snapshot)"
                 await _apply_default_config()

        else:
            logger.info(f"Snapshot {SNAPSHOT_FILE} no encontrado. Restaurando a valores por defecto.")
            config_source = "defaults (no snapshot)"
            await _apply_default_config()

        if hasattr(settings, 'reload') and callable(settings.reload):
            logger.info("Intentando recargar configuración llamando a settings.reload()...")
            if asyncio.iscoroutinefunction(settings.reload):
                await settings.reload()
            else:
                settings.reload()
            logger.info("Llamada a settings.reload() completada.")

        logger.info(f"Configuración restaurada usando: {config_source}")

    except Exception as e:
        logger.error(f"Error general al restaurar configuración: {e}")
        raise

async def _apply_default_config():
    """Aplica la configuración por defecto como fallback."""
    logger.info("Aplicando configuración por defecto...")
    defaults_settings = {
        "ELEVENLABS_MAX_RETRIES": 3,
        "ELEVENLABS_CONNECTION_TIMEOUT": 30,
        "ELEVENLABS_POOL_SIZE": 10
    }
    defaults_env = {}

    for k, v in defaults_env.items():
         if k.startswith("ELEVENLABS_"):
             os.environ[k] = str(v) if v is not None else ""
             logger.debug(f"[Default] os.environ['{k}'] = '{os.environ[k]}'")

    for k, v in defaults_settings.items():
        if hasattr(settings, k):
            setattr(settings, k, v)
            logger.debug(f"[Default] settings.{k} = {v}")
        else:
             logger.warning(f"[Default] El atributo '{k}' no existe en el objeto settings.")
