from collections.abc import AsyncGenerator
from functools import lru_cache

from fastapi import Depends

from app.config.settings import get_settings
from app.services.call_service import CallService
from app.services.campaign_scheduler import CampaignScheduler
from app.services.campaign_service import CampaignService
from app.services.contact_service import ContactService
from app.services.twilio_service import TwilioService  # Importar TwilioService
from supabase import Client, create_client

settings = get_settings()


@lru_cache
async def get_supabase_client() -> Client:
    """
    Returns a cached Supabase client instance
    """
    return create_client(supabase_url=settings.SUPABASE_URL, supabase_key=settings.SUPABASE_KEY)


@lru_cache
async def get_twilio_service() -> TwilioService:  # Cambiar nombre y tipo de retorno
    """
    Returns a cached Twilio service instance
    """
    return TwilioService()  # Devolver instancia de TwilioService


@lru_cache
async def get_campaign_service(supabase: Client = Depends(get_supabase_client)) -> CampaignService:
    """
    Returns a cached Campaign service instance
    """
    return CampaignService(supabase)


@lru_cache
async def get_call_service(
    supabase: Client = Depends(get_supabase_client),
    twilio: TwilioService = Depends(get_twilio_service),  # Usar TwilioService y la nueva función
) -> CallService:
    """
    Returns a cached Call service instance
    """
    return CallService(supabase, twilio)


@lru_cache
async def get_contact_service(supabase: Client = Depends(get_supabase_client)):
    """
    Returns a cached Contact service instance
    """
    return ContactService(supabase)


async def get_campaign_scheduler(
    campaign_service: CampaignService = Depends(get_campaign_service),
    call_service: CallService = Depends(get_call_service),
    contact_service: ContactService = Depends(get_contact_service),
) -> AsyncGenerator[CampaignScheduler, None]:
    """
    Returns a CampaignScheduler instance and manages its lifecycle
    """
    scheduler = CampaignScheduler(
        campaign_service=campaign_service,
        call_service=call_service,
        contact_service=contact_service,
        check_interval=settings.SCHEDULER_CHECK_INTERVAL,
    )

    await scheduler.start()
    try:
        yield scheduler
    finally:
        await scheduler.stop()
