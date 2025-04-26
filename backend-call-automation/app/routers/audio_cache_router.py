"""
Router para la gestión del caché de audio.

Este módulo define los endpoints para gestionar el caché de audio,
incluyendo estadísticas y operaciones de limpieza.
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from app.services.audio_cache_service import audio_cache_service
from app.config.dependencies import get_supabase_client
from app.utils.logging import app_logger as logger
from supabase import Client as SupabaseClient

router = APIRouter(prefix="/api/audio-cache", tags=["audio-cache"])

@router.get("/stats", response_model=Dict[str, Any])
async def get_cache_stats(
    supabase_client: SupabaseClient = Depends(get_supabase_client)
) -> Dict[str, Any]:
    """
    Obtiene estadísticas del caché de audio.
    
    Returns:
        Dict con estadísticas del caché
    """
    try:
        stats = await audio_cache_service.get_cache_stats()
        return stats
    except Exception as e:
        logger.error(f"Error al obtener estadísticas del caché: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas del caché: {str(e)}"
        )

@router.post("/clear", response_model=Dict[str, bool])
async def clear_cache(
    supabase_client: SupabaseClient = Depends(get_supabase_client)
) -> Dict[str, bool]:
    """
    Limpia todo el caché de audio.
    
    Returns:
        Dict con confirmación de limpieza
    """
    try:
        success = await audio_cache_service.clear_cache()
        return {"success": success}
    except Exception as e:
        logger.error(f"Error al limpiar el caché: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al limpiar el caché: {str(e)}"
        )
