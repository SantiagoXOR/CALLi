"""
Router para reportes y estadísticas.

Este módulo define los endpoints para obtener reportes y estadísticas
sobre campañas, llamadas y contactos.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from fastapi.responses import JSONResponse, StreamingResponse
import io
import csv
import pandas as pd
from app.services.call_service import CallService
from app.services.campaign_service import CampaignService
from app.services.contact_service import ContactService
from app.config.dependencies import get_call_service, get_campaign_service, get_contact_service

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/campaign/{campaign_id}/summary", response_model=Dict[str, Any])
async def get_campaign_summary(
    campaign_id: str = Path(..., description="ID de la campaña"),
    campaign_service: CampaignService = Depends(get_campaign_service),
    call_service: CallService = Depends(get_call_service)
) -> Dict[str, Any]:
    """
    Obtiene un resumen de una campaña específica.
    
    - **campaign_id**: ID único de la campaña
    
    Returns:
        Dict con resumen de la campaña
    """
    # Obtener detalles de la campaña
    campaign = await campaign_service.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaña no encontrada"
        )
    
    # Obtener métricas de llamadas para la campaña
    call_metrics = await call_service.get_call_metrics(campaign_id=campaign_id)
    
    # Calcular tasas
    total_calls = sum(call_metrics.get("by_status", {}).values())
    success_rate = (call_metrics.get("by_status", {}).get("completed", 0) / total_calls) * 100 if total_calls > 0 else 0
    failure_rate = (call_metrics.get("by_status", {}).get("failed", 0) / total_calls) * 100 if total_calls > 0 else 0
    
    # Construir resumen
    return {
        "campaign": {
            "id": campaign.id,
            "name": campaign.name,
            "description": campaign.description,
            "status": campaign.status,
            "created_at": campaign.created_at,
            "updated_at": campaign.updated_at
        },
        "metrics": {
            "total_calls": total_calls,
            "completed_calls": call_metrics.get("by_status", {}).get("completed", 0),
            "failed_calls": call_metrics.get("by_status", {}).get("failed", 0),
            "in_progress_calls": call_metrics.get("by_status", {}).get("in_progress", 0),
            "queued_calls": call_metrics.get("by_status", {}).get("queued", 0),
            "cancelled_calls": call_metrics.get("by_status", {}).get("cancelled", 0),
            "success_rate": round(success_rate, 2),
            "failure_rate": round(failure_rate, 2),
            "avg_duration": call_metrics.get("avg_duration", 0)
        },
        "timeline": call_metrics.get("timeline", [])
    }

@router.get("/campaigns/performance", response_model=List[Dict[str, Any]])
async def get_campaigns_performance(
    start_date: Optional[datetime] = Query(None, description="Filtrar desde fecha (formato ISO)"),
    end_date: Optional[datetime] = Query(None, description="Filtrar hasta fecha (formato ISO)"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de campañas"),
    campaign_service: CampaignService = Depends(get_campaign_service),
    call_service: CallService = Depends(get_call_service)
) -> List[Dict[str, Any]]:
    """
    Obtiene métricas de rendimiento para todas las campañas.
    
    - **start_date**: Filtrar desde fecha (formato ISO)
    - **end_date**: Filtrar hasta fecha (formato ISO)
    - **limit**: Número máximo de campañas a devolver
    
    Returns:
        Lista de campañas con sus métricas de rendimiento
    """
    # Si no se especifica end_date, usar fecha actual
    if not end_date:
        end_date = datetime.now()
    
    # Si no se especifica start_date, usar 30 días antes de end_date
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # Obtener campañas
    campaigns = await campaign_service.list_campaigns(
        filters={"start_date": start_date, "end_date": end_date},
        limit=limit
    )
    
    # Obtener métricas para cada campaña
    result = []
    for campaign in campaigns:
        # Obtener métricas de llamadas para la campaña
        call_metrics = await call_service.get_call_metrics(
            campaign_id=campaign.id,
            start_date=start_date,
            end_date=end_date
        )
        
        # Calcular tasas
        total_calls = sum(call_metrics.get("by_status", {}).values())
        success_rate = (call_metrics.get("by_status", {}).get("completed", 0) / total_calls) * 100 if total_calls > 0 else 0
        
        # Añadir a resultados
        result.append({
            "id": campaign.id,
            "name": campaign.name,
            "status": campaign.status,
            "total_calls": total_calls,
            "success_rate": round(success_rate, 2),
            "avg_duration": call_metrics.get("avg_duration", 0)
        })
    
    # Ordenar por tasa de éxito descendente
    result.sort(key=lambda x: x["success_rate"], reverse=True)
    
    return result

@router.get("/call_history", response_model=Dict[str, Any])
async def get_call_history(
    campaign_id: Optional[str] = Query(None, description="Filtrar por ID de campaña"),
    contact_id: Optional[str] = Query(None, description="Filtrar por ID de contacto"),
    start_date: Optional[datetime] = Query(None, description="Filtrar desde fecha (formato ISO)"),
    end_date: Optional[datetime] = Query(None, description="Filtrar hasta fecha (formato ISO)"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    call_service: CallService = Depends(get_call_service)
) -> Dict[str, Any]:
    """
    Obtiene el historial de llamadas con filtros.
    
    - **campaign_id**: Filtrar por ID de campaña (opcional)
    - **contact_id**: Filtrar por ID de contacto (opcional)
    - **start_date**: Filtrar desde fecha (formato ISO)
    - **end_date**: Filtrar hasta fecha (formato ISO)
    - **page**: Número de página (comienza en 1)
    - **page_size**: Tamaño de página (entre 1 y 100)
    
    Returns:
        Dict con historial de llamadas y metadatos de paginación
    """
    # Si no se especifica end_date, usar fecha actual
    if not end_date:
        end_date = datetime.now()
    
    # Si no se especifica start_date, usar 30 días antes de end_date
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # Obtener historial de llamadas
    calls, total = await call_service.list_calls(
        campaign_id=campaign_id,
        contact_id=contact_id,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size,
        sort_by="created_at",
        sort_order="desc"
    )
    
    return {
        "data": calls,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size if page_size > 0 else 1
    }

@router.get("/export/calls", response_class=StreamingResponse)
async def export_call_history(
    campaign_id: Optional[str] = Query(None, description="Filtrar por ID de campaña"),
    start_date: Optional[datetime] = Query(None, description="Filtrar desde fecha (formato ISO)"),
    end_date: Optional[datetime] = Query(None, description="Filtrar hasta fecha (formato ISO)"),
    format: str = Query("csv", description="Formato de exportación (csv, excel)"),
    call_service: CallService = Depends(get_call_service),
    campaign_service: CampaignService = Depends(get_campaign_service),
    contact_service: ContactService = Depends(get_contact_service)
) -> StreamingResponse:
    """
    Exporta el historial de llamadas a CSV o Excel.
    
    - **campaign_id**: Filtrar por ID de campaña (opcional)
    - **start_date**: Filtrar desde fecha (formato ISO)
    - **end_date**: Filtrar hasta fecha (formato ISO)
    - **format**: Formato de exportación (csv, excel)
    
    Returns:
        Archivo CSV o Excel con el historial de llamadas
    """
    # Si no se especifica end_date, usar fecha actual
    if not end_date:
        end_date = datetime.now()
    
    # Si no se especifica start_date, usar 30 días antes de end_date
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # Obtener todas las llamadas (sin paginación)
    calls, _ = await call_service.list_calls(
        campaign_id=campaign_id,
        start_date=start_date,
        end_date=end_date,
        page=1,
        page_size=10000,  # Valor alto para obtener todas
        sort_by="created_at",
        sort_order="desc"
    )
    
    # Convertir a DataFrame
    calls_data = [call.dict() for call in calls]
    df = pd.DataFrame(calls_data)
    
    # Añadir información de campaña si existe
    if campaign_id:
        campaign = await campaign_service.get_campaign(campaign_id)
        if campaign:
            df["campaign_name"] = campaign.name
    
    # Preparar respuesta según formato
    if format.lower() == "excel":
        # Exportar a Excel
        output = io.BytesIO()
        df.to_excel(output, index=False, engine="openpyxl")
        output.seek(0)
        
        filename = f"call_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        
        return StreamingResponse(
            output,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    else:
        # Exportar a CSV (por defecto)
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        filename = f"call_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode("utf-8")),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

@router.get("/performance_metrics", response_model=Dict[str, Any])
async def get_performance_metrics(
    start_date: Optional[datetime] = Query(None, description="Filtrar desde fecha (formato ISO)"),
    end_date: Optional[datetime] = Query(None, description="Filtrar hasta fecha (formato ISO)"),
    campaign_id: Optional[str] = Query(None, description="Filtrar por ID de campaña"),
    call_service: CallService = Depends(get_call_service)
) -> Dict[str, Any]:
    """
    Obtiene métricas de rendimiento general.
    
    - **start_date**: Filtrar desde fecha (formato ISO)
    - **end_date**: Filtrar hasta fecha (formato ISO)
    - **campaign_id**: Filtrar por ID de campaña (opcional)
    
    Returns:
        Dict con métricas de rendimiento
    """
    # Si no se especifica end_date, usar fecha actual
    if not end_date:
        end_date = datetime.now()
    
    # Si no se especifica start_date, usar 30 días antes de end_date
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # Obtener métricas
    metrics = await call_service.get_call_metrics(
        campaign_id=campaign_id,
        start_date=start_date,
        end_date=end_date,
        group_by="day"
    )
    
    # Calcular métricas adicionales
    total_calls = sum(metrics.get("by_status", {}).values())
    completed_calls = metrics.get("by_status", {}).get("completed", 0)
    failed_calls = metrics.get("by_status", {}).get("failed", 0)
    
    success_rate = (completed_calls / total_calls) * 100 if total_calls > 0 else 0
    failure_rate = (failed_calls / total_calls) * 100 if total_calls > 0 else 0
    
    # Construir respuesta
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": (end_date - start_date).days
        },
        "summary": {
            "total_calls": total_calls,
            "completed_calls": completed_calls,
            "failed_calls": failed_calls,
            "success_rate": round(success_rate, 2),
            "failure_rate": round(failure_rate, 2),
            "avg_duration": metrics.get("avg_duration", 0),
            "calls_per_day": round(total_calls / (end_date - start_date).days, 2) if (end_date - start_date).days > 0 else 0
        },
        "by_status": metrics.get("by_status", {}),
        "timeline": metrics.get("timeline", [])
    }
