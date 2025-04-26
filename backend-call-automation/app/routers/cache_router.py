from fastapi import APIRouter, Depends, HTTPException

from app.services.cache_service import cache_service
from app.models.cache_metrics import CacheMetrics

router = APIRouter(
    prefix="/cache",
    tags=["cache"],
    responses={404: {"description": "Not found"}},
)

@router.get("/metrics", response_model=CacheMetrics)
async def get_cache_metrics():
    """Obtiene las métricas actuales de la caché."""
    return await cache_service.get_metrics()

@router.post("/sync")
async def force_sync(table_name: str, key_prefix: str = None):
    """Fuerza una sincronización inmediata con Supabase."""
    success = await cache_service.force_sync(table_name, key_prefix)
    if not success:
        raise HTTPException(status_code=500, detail="Error al sincronizar con Supabase")
    return {"status": "success", "message": "Sincronización completada"}

@router.post("/clear")
async def clear_cache():
    """Limpia toda la caché."""
    success = await cache_service.clear_all_cache()
    if not success:
        raise HTTPException(status_code=500, detail="Error al limpiar la caché")
    return {"status": "success", "message": "Caché limpiada correctamente"}

@router.post("/preload/{conversation_id}")
async def preload_conversation(conversation_id: str):
    """Precarga una conversación desde Supabase a la caché."""
    success = await cache_service.preload_conversation(conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversación no encontrada o error al precargar")
    return {"status": "success", "message": "Conversación precargada correctamente"}
