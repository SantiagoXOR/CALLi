"""Servicio para la gestión de campañas de llamadas automatizadas."""

from datetime import datetime
from uuid import UUID
from fastapi import HTTPException, status
from app.models.campaign import Campaign, CampaignCreate, CampaignUpdate, CampaignStatus
from typing import Optional

class CampaignService:
    """Servicio para gestionar campañas de llamadas automatizadas.
    
    Este servicio proporciona métodos para crear, consultar, actualizar y eliminar campañas,
    así como para gestionar sus estadísticas y estado.
    
    Attributes:
        supabase: Cliente de Supabase para la persistencia de datos
    """
    def __init__(self, supabase_client):
        """Inicializa el servicio de campañas.
        
        Args:
            supabase_client: Cliente de Supabase para la persistencia de datos
        """
        self.supabase = supabase_client
        self.table_name = "campaigns"

    async def create_campaign(self, campaign: CampaignCreate) -> Campaign:
        """Crea una nueva campaña de llamadas.
        
        Args:
            campaign: Datos de la campaña a crear
            
        Returns:
            Campaign: La campaña creada con su ID asignado
            
        Raises:
            HTTPException: Si hay un error al crear la campaña
        """
        try:
            result = self.supabase.from_table(self.table_name).insert(campaign.model_dump()).execute()
            if result and result["data"]:
                return Campaign(**result["data"][0])
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear la campaña"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear la campaña: {str(e)}"
            )

    async def get_campaign(self, campaign_id: UUID) -> Campaign:
        """Obtiene una campaña por su ID.
        
        Args:
            campaign_id: ID de la campaña a obtener (UUID)
            
        Returns:
            Campaign: La campaña encontrada
            
        Raises:
            HTTPException: Si la campaña no existe o hay un error al obtenerla
        """
        try:
            result = self.supabase.from_table(self.table_name).select("*").eq("id", str(campaign_id)).execute()
            if result and result["data"]:
                return Campaign(**result["data"][0])
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaña no encontrada"
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener la campaña: {str(e)}"
            )

    async def list_campaigns(
        self,
        page: int = 1,
        page_size: int = 10,
        status: Optional[CampaignStatus] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> list[Campaign]:
        """Lista campañas con filtros y paginación.
        
        Args:
            page: Número de página actual (default: 1)
            page_size: Tamaño de página (default: 10)
            status: Filtro por estado de la campaña
            start_date: Filtro por fecha de inicio mínima
            end_date: Filtro por fecha de fin máxima
            
        Returns:
            list[Campaign]: Lista de campañas que cumplen los criterios
            
        Raises:
            HTTPException: Si hay un error al listar las campañas
        """
        try:
            query = self.supabase.from_table(self.table_name).select("*")

            if status:
                query = query.eq("status", status.value)
            if start_date:
                query = query.gte("schedule_start", start_date.isoformat())
            if end_date:
                query = query.lte("schedule_end", end_date.isoformat())

            offset = (page - 1) * page_size
            query = query.range(offset, offset + page_size - 1)

            result = query.execute()
            if result and result["data"]:
                return [Campaign(**item) for item in result["data"]]
            return []
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al listar las campañas: {str(e)}"
            )

    async def update_campaign(self, campaign_id: UUID, campaign_update: CampaignUpdate) -> Campaign:
        """Actualiza una campaña existente.
        
        Args:
            campaign_id: ID de la campaña a actualizar (UUID)
            campaign_update: Datos actualizados de la campaña
            
        Returns:
            Campaign: La campaña actualizada
            
        Raises:
            HTTPException: Si la campaña no existe o hay un error al actualizarla
        """
        try:
            # Primero verificamos que la campaña existe
            await self.get_campaign(campaign_id)

            # Actualizamos solo los campos no nulos
            update_data = {k: v for k, v in campaign_update.model_dump(exclude_unset=True).items()}
            result = self.supabase.from_table(self.table_name).update(update_data).eq("id", str(campaign_id)).execute()

            if result and result["data"]:
                return Campaign(**result["data"][0])
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaña no encontrada"
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar la campaña: {str(e)}"
            )

    async def delete_campaign(self, campaign_id: UUID) -> bool:
        """Elimina una campaña existente.
        
        Args:
            campaign_id: ID de la campaña a eliminar (UUID)
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
            
        Raises:
            HTTPException: Si hay un error al eliminar la campaña
        """
        try:
            # Primero verificamos que la campaña existe
            await self.get_campaign(campaign_id)

            result = self.supabase.from_table(self.table_name).delete().eq("id", str(campaign_id)).execute()
            if result and result["data"]:
                return True
            return False
        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar la campaña: {str(e)}"
            )

    async def update_campaign_stats(
        self,
        campaign_id: UUID,
        total_calls: int,
        successful_calls: int,
        failed_calls: int,
        pending_calls: int
    ) -> Campaign:
        """Actualiza las estadísticas de una campaña.
        
        Args:
            campaign_id: ID de la campaña (UUID)
            total_calls: Total de llamadas realizadas
            successful_calls: Llamadas exitosas
            failed_calls: Llamadas fallidas
            pending_calls: Llamadas pendientes
            
        Returns:
            Campaign: La campaña con estadísticas actualizadas
            
        Raises:
            HTTPException: Si hay error de validación o al actualizar
        """
        try:
            # Validar las estadísticas
            if (successful_calls + failed_calls > total_calls or
                any(x < 0 for x in [total_calls, successful_calls, failed_calls, pending_calls])):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Estadísticas inválidas"
                )

            stats = {
                "total_calls": total_calls,
                "successful_calls": successful_calls,
                "failed_calls": failed_calls,
                "pending_calls": pending_calls
            }

            result = self.supabase.from_table(self.table_name).update(stats).eq("id", str(campaign_id)).execute()
            if result and result["data"]:
                return Campaign(**result["data"][0])
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaña no encontrada"
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar las estadísticas: {str(e)}"
            )
