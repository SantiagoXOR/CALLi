from fastapi import APIRouter, Depends, status
from datetime import datetime
from uuid import UUID
from app.models.campaign import Campaign, CampaignCreate, CampaignUpdate, CampaignStatus
from app.services.campaign_service import CampaignService
from app.config.database import get_supabase_client

router = APIRouter(prefix="/api/campaigns", tags=["campaigns"])

@router.post("/", response_model=Campaign, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign: CampaignCreate,
    supabase_client = Depends(get_supabase_client)
) -> Campaign:
    """
    Crea una nueva campaña.
    
    Parámetros:
    - **name**: Nombre de la campaña (requerido)
    - **description**: Descripción opcional
    - **status**: Estado inicial (default: DRAFT)
    - **schedule_start**: Fecha/hora de inicio (requerido)
    - **schedule_end**: Fecha/hora de fin (requerido)
    - **contact_list_ids**: Lista de IDs de contactos (UUID)
    - **script_template**: Plantilla del script (requerido)
    - **max_retries**: Máximo de reintentos (default: 3)
    - **retry_delay_minutes**: Tiempo entre reintentos (default: 60)
    - **calling_hours_start**: Hora inicio llamadas (HH:MM)
    - **calling_hours_end**: Hora fin llamadas (HH:MM)
    """
    campaign_service = CampaignService(supabase_client)
    return await campaign_service.create_campaign(campaign)

@router.get("/{campaign_id}", response_model=Campaign)
async def get_campaign(
    campaign_id: UUID,
    supabase_client = Depends(get_supabase_client)
) -> Campaign:
    """
    Obtiene una campaña por su ID.
    """
    campaign_service = CampaignService(supabase_client)
    return await campaign_service.get_campaign(campaign_id)

@router.get("/", response_model=list[Campaign])
async def list_campaigns(
    page: int = 1,
    page_size: int = 10,
    status: CampaignStatus | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    supabase_client = Depends(get_supabase_client)
) -> list[Campaign]:
    """
    Lista las campañas con filtros opcionales.
    
    Parámetros:
    - **page**: Número de página (default: 1)
    - **page_size**: Tamaño de página (default: 10)
    - **status**: Filtrar por estado
    - **start_date**: Filtrar por fecha de inicio
    - **end_date**: Filtrar por fecha de fin
    """
    campaign_service = CampaignService(supabase_client)
    return await campaign_service.list_campaigns(
        page=page,
        page_size=page_size,
        status=status,
        start_date=start_date,
        end_date=end_date
    )

@router.patch("/{campaign_id}", response_model=Campaign)
async def update_campaign(
    campaign_id: UUID,
    campaign_update: CampaignUpdate,
    supabase_client = Depends(get_supabase_client)
) -> Campaign:
    """
    Actualiza una campaña existente.
    
    Campos actualizables:
    - name
    - description
    - status
    - schedule_start
    - schedule_end
    - contact_list_ids
    - script_template
    - max_retries
    - retry_delay_minutes
    - calling_hours_start
    - calling_hours_end
    """
    campaign_service = CampaignService(supabase_client)
    return await campaign_service.update_campaign(campaign_id, campaign_update)

@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(
    campaign_id: UUID,
    supabase_client = Depends(get_supabase_client)
) -> None:
    """
    Elimina una campaña.
    """
    campaign_service = CampaignService(supabase_client)
    await campaign_service.delete_campaign(campaign_id)

@router.patch("/{campaign_id}/stats", response_model=Campaign)
async def update_campaign_stats(
    campaign_id: UUID,
    total_calls: int,
    successful_calls: int,
    failed_calls: int,
    pending_calls: int,
    supabase_client = Depends(get_supabase_client)
) -> Campaign:
    """
    Actualiza las estadísticas de una campaña.
    
    Parámetros:
    - **total_calls**: Total de llamadas realizadas
    - **successful_calls**: Llamadas exitosas
    - **failed_calls**: Llamadas fallidas
    - **pending_calls**: Llamadas pendientes
    """
    campaign_service = CampaignService(supabase_client)
    return await campaign_service.update_campaign_stats(
        campaign_id,
        total_calls,
        successful_calls,
        failed_calls,
        pending_calls
    )
