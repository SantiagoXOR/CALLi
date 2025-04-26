from datetime import datetime, timedelta
from typing import List, Optional
import logging
import asyncio
from fastapi import HTTPException
from app.models.campaign import Campaign, CampaignStatus
from app.models.call import Call, CallStatus, CallCreate
from app.services.campaign_service import CampaignService
from app.services.call_service import CallService
# from app.services.contact_service import ContactService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CampaignScheduler:
    """
    Planificador de campañas que gestiona y ejecuta campañas de llamadas automáticas.

    Incluye la lógica para procesar campañas activas, reintentar llamadas fallidas y actualizar las estadísticas de las campañas.

    Attributes:
        campaign_service (CampaignService): Servicio para gestionar campañas.
        call_service (CallService): Servicio para gestionar llamadas.
        check_interval (int): Intervalo en segundos para revisar campañas activas.
        max_concurrent_calls (int): Número máximo de llamadas simultáneas permitidas.
        retry_delay (int): Tiempo en minutos entre reintentos de llamadas.
        max_retries (int): Número máximo de reintentos permitidos por llamada.

    Dependencies:
        - Supabase: Para la persistencia de datos
        - CallService: Para la gestión de llamadas individuales
    """

    def __init__(
        self,
        campaign_service: CampaignService,
        call_service: CallService,
        # contact_service: ContactService,
        check_interval: int = 60,
        max_concurrent_calls: int = 10,
        retry_delay: int = 15,
        max_retries: int = 3
    ):
        """
        Inicializa el planificador de campañas.

        Args:
            campaign_service (CampaignService): Servicio para gestionar campañas.
            call_service (CallService): Servicio para gestionar llamadas.
            contact_service (ContactService): Servicio para gestionar contactos.
            check_interval (int): Intervalo en segundos para revisar campañas.
            max_concurrent_calls (int): Máximo de llamadas simultáneas.
            retry_delay (int): Minutos entre reintentos.
            max_retries (int): Máximo de reintentos por llamada.
        """
        self.campaign_service = campaign_service
        self.call_service = call_service
        self.contact_service = contact_service
        self.check_interval = check_interval
        self.max_concurrent_calls = max_concurrent_calls
        self.retry_delay = retry_delay
        self.max_retries = max_retries
        self.is_running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """
        Inicia el planificador de campañas.

        Este método inicia un bucle asíncrono que periódicamente revisa y procesa
        las campañas activas.

        Returns:
            None

        Raises:
            RuntimeError: Si el planificador ya está en ejecución
        """
        if self.is_running:
            raise RuntimeError("El planificador ya está en ejecución")
        
        self.is_running = True
        self._task = asyncio.create_task(self._run())
        logger.info("Planificador de campañas iniciado")

    async def stop(self) -> None:
        """
        Detiene el planificador de campañas.

        Returns:
            None
        """
        if not self.is_running:
            return

        self.is_running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Planificador de campañas detenido")

    async def _run(self) -> None:
        """
        Ejecuta el bucle principal del planificador.

        Procesa campañas activas y reintenta llamadas fallidas en intervalos regulares.

        Returns:
            None
        """
        while self.is_running:
            try:
                await self._process_active_campaigns()
                await self._retry_failed_calls()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error en el planificador: {str(e)}")
                await asyncio.sleep(self.check_interval)

    async def _process_active_campaigns(self) -> None:
        """
        Procesa todas las campañas activas.

        Este método:
        1. Obtiene todas las campañas activas
        2. Para cada campaña, procesa las llamadas pendientes
        3. Actualiza las estadísticas de las campañas

        Returns:
            None

        Raises:
            Exception: Si hay un error al procesar las campañas
        """
        try:
            # Obtener campañas activas dentro del horario programado
            now = datetime.now()
            campaigns = await self.campaign_service.list_campaigns(
                status=CampaignStatus.ACTIVE,
                start_date=now,
                end_date=now
            )

            for campaign in campaigns:
                await self._process_campaign(campaign)

        except Exception as e:
            logger.error(f"Error al procesar campañas activas: {str(e)}")

    async def _process_campaign(self, campaign: Campaign) -> None:
        """
        Procesa una campaña individual.

        Args:
            campaign (Campaign): Campaña a procesar

        Returns:
            None

        Raises:
            Exception: Si hay un error al procesar la campaña
        """
        try:
            # Verificar si hay contactos pendientes
            if campaign.pending_calls <= 0:
                logger.info(f"Campaña {campaign.id} no tiene llamadas pendientes")
                # Marcar como completada si no hay más llamadas pendientes
                await self.campaign_service.update_campaign(
                    campaign.id,
                    {"status": CampaignStatus.COMPLETED}
                )
                return

            # Obtener contactos de la campaña que no han sido llamados o necesitan reintento
            contacts = await self.contact_service.get_campaign_contacts(campaign.id)

            # Filtrar contactos que no han sido llamados o necesitan reintento
            for contact in contacts:
                try:
                    # Verificar si el contacto ya fue llamado
                    result = await self.supabase.from_("campaign_contacts")\
                        .select("*")\
                        .eq("campaign_id", campaign.id)\
                        .eq("contact_id", contact.id)\
                        .single()\
                        .execute()

                    if result and result["data"]:
                        contact_status = result["data"]
                        # Saltar si ya fue llamado exitosamente o alcanzó el máximo de reintentos
                        if (contact_status["call_status"] == "completed" or
                            contact_status["retry_count"] >= campaign.max_retries):
                            continue

                    call_data = CallCreate(
                        campaign_id=campaign.id,
                        phone_number=contact.phone_number,
                        from_number="+15005550006",  # Número de Twilio (debería venir de la configuración)
                        webhook_url=f"https://api.example.com/webhook/{campaign.id}/{contact.id}",
                        status_callback_url=f"https://api.example.com/callback/{campaign.id}/{contact.id}",
                        max_retries=campaign.max_retries,
                        retry_attempts=result["data"]["retry_count"] if result and result["data"] else 0
                    )

                    # Crear la llamada
                    call = await self.call_service.create_call(call_data)

                    # Actualizar el estado en campaign_contacts
                    await self.supabase.from_("campaign_contacts")\
                        .upsert({
                            "campaign_id": campaign.id,
                            "contact_id": contact.id,
                            "called_at": datetime.now().isoformat(),
                            "call_status": call.status.value,
                            "retry_count": call_data.retry_attempts + 1
                        })\
                        .execute()

                except Exception as e:
                    logger.error(f"Error al crear llamada para contacto {contact.id}: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"Error al procesar campaña {campaign.id}: {str(e)}")

    async def _retry_failed_calls(self) -> None:
        """
        Reintenta las llamadas fallidas que cumplen con los criterios de reintento.

        Verifica el tiempo de espera entre reintentos y reintenta las llamadas fallidas.

        Returns:
            None

        Raises:
            Exception: Si hay un error al procesar reintentos
        """
        try:
            # Obtener llamadas fallidas
            failed_calls = await self.call_service.list_calls(
                status=CallStatus.FAILED
            )

            now = datetime.now()
            for call in failed_calls:
                # Verificar si se puede reintentar
                if not await self.call_service.is_retry_allowed(call):
                    continue

                # Verificar el tiempo de espera entre reintentos
                campaign = await self.campaign_service.get_campaign(call.campaign_id)
                last_attempt = datetime.fromisoformat(str(call.updated_at))
                retry_delay = timedelta(minutes=campaign.retry_delay_minutes)

                if now - last_attempt < retry_delay:
                    continue

                # Reintentar la llamada
                try:
                    await self.call_service.retry_call(call.id)
                except Exception as e:
                    logger.error(f"Error al reintentar llamada {call.id}: {str(e)}")

        except Exception as e:
            logger.error(f"Error al procesar reintentos: {str(e)}")

    async def update_campaign_stats(self, campaign_id: int) -> None:
        """
        Actualiza las estadísticas de una campaña.

        Obtiene las métricas de llamadas y actualiza las estadísticas de la campaña en la base de datos.

        Args:
            campaign_id (int): ID de la campaña

        Returns:
            None

        Raises:
            Exception: Si hay un error al actualizar estadísticas de campaña
        """
        try:
            # Obtener métricas de llamadas
            metrics = await self.call_service.get_call_metrics(campaign_id)

            # Actualizar estadísticas de la campaña
            await self.campaign_service.update_campaign_stats(
                campaign_id,
                {
                    "total_calls": metrics.total_calls,
                    "successful_calls": metrics.completed_calls,
                    "failed_calls": metrics.failed_calls,
                    "pending_calls": metrics.total_calls - (metrics.completed_calls + metrics.failed_calls)
                }
            )
        except Exception as e:
            logger.error(f"Error al actualizar estadísticas de campaña {campaign_id}: {str(e)}")
