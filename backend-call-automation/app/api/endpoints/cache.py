from fastapi import APIRouter, HTTPException, BackgroundTasks
import logging
from datetime import datetime

from app.config.redis_client import get_redis_client
from app.config.supabase import get_supabase_client
from app.services.cache_service import CacheService


router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/cache/preload/{conversation_id}")
async def preload_conversation(conversation_id: str, background_tasks: BackgroundTasks):
    """
    Implementa precarga predictiva de conversaciones específicas
    
    Args:
        conversation_id: ID de la conversación a precargar
        background_tasks: Tareas en segundo plano
        
    Returns:
        Dict: Estado de la operación de precarga
    """
    try:
        # Obtener servicios necesarios
        redis_client = get_redis_client()
        supabase_client = get_supabase_client()
        cache_service = CacheService(redis_client, supabase_client)
        
        # Iniciar precarga en segundo plano
        background_tasks.add_task(
            cache_service.preload_conversation_data,
            conversation_id
        )
        
        return {
            "status": "success",
            "message": f"Precarga de conversación {conversation_id} iniciada",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error en precarga: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al iniciar precarga: {str(e)}"
        )

@router.post("/cache/sync")
async def force_sync(background_tasks: BackgroundTasks):
    """
    Implementa sincronización forzada entre caché y almacenamiento persistente
    
    Args:
        background_tasks: Tareas en segundo plano
        
    Returns:
        Dict: Estado de la operación de sincronización
    """
    try:
        # Obtener servicios necesarios
        redis_client = get_redis_client()
        supabase_client = get_supabase_client()
        cache_service = CacheService(redis_client, supabase_client)
        
        # Iniciar sincronización asíncrona por lotes en segundo plano
        background_tasks.add_task(
            cache_service.force_sync_to_persistent_storage,
            batch_size=10  # Configurable según necesidades
        )
        
        return {
            "status": "success",
            "message": "Sincronización forzada iniciada",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error en sincronización: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al iniciar sincronización: {str(e)}"
        )

@router.get("/cache/metrics")
async def get_cache_metrics():
    """
    Obtiene métricas actuales del sistema de caché
    
    Returns:
        CacheMetrics: Métricas del sistema de caché
    """
    try:
        # Obtener servicios necesarios
        redis_client = get_redis_client()
        supabase_client = get_supabase_client()
        cache_service = CacheService(redis_client, supabase_client)
        
        # Obtener métricas actuales
        metrics = await cache_service.get_metrics()
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error al obtener métricas: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener métricas: {str(e)}"
        )
