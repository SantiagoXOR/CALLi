"""
Dependencias de servicios para la inyección de dependencias en FastAPI.
"""

from typing import Annotated

from fastapi import Depends

from app.services.ai_conversation_service import AIConversationService
from app.services.audio_cache_service import AudioCacheService
from app.services.call_service import CallService
from app.services.campaign_service import CampaignService
from app.services.contact_service import ContactService
from app.services.elevenlabs_service import ElevenLabsService
from app.services.enhanced_ai_conversation_service import EnhancedAIConversationService
from app.services.twilio_service import TwilioService

# Singleton instances
_call_service = None
_twilio_service = None
_campaign_service = None
_contact_service = None
_ai_conversation_service = None
_enhanced_ai_conversation_service = None
_elevenlabs_service = None
_audio_cache_service = None


async def get_call_service() -> CallService:
    """
    Obtiene una instancia singleton del servicio de llamadas.

    Returns:
        CallService: Instancia del servicio de llamadas
    """
    global _call_service
    if _call_service is None:
        _call_service = CallService()
    return _call_service


async def get_twilio_service() -> TwilioService:
    """
    Obtiene una instancia singleton del servicio de Twilio.

    Returns:
        TwilioService: Instancia del servicio de Twilio
    """
    global _twilio_service
    if _twilio_service is None:
        _twilio_service = TwilioService()
    return _twilio_service


async def get_campaign_service() -> CampaignService:
    """
    Obtiene una instancia singleton del servicio de campañas.

    Returns:
        CampaignService: Instancia del servicio de campañas
    """
    global _campaign_service
    if _campaign_service is None:
        _campaign_service = CampaignService()
    return _campaign_service


async def get_contact_service() -> ContactService:
    """
    Obtiene una instancia singleton del servicio de contactos.

    Returns:
        ContactService: Instancia del servicio de contactos
    """
    global _contact_service
    if _contact_service is None:
        _contact_service = ContactService()
    return _contact_service


async def get_ai_conversation_service() -> AIConversationService:
    """
    Obtiene una instancia singleton del servicio de conversación con IA.

    Returns:
        AIConversationService: Instancia del servicio de conversación con IA
    """
    global _ai_conversation_service
    if _ai_conversation_service is None:
        _ai_conversation_service = AIConversationService()
    return _ai_conversation_service


async def get_enhanced_ai_conversation_service() -> EnhancedAIConversationService:
    """
    Obtiene una instancia singleton del servicio mejorado de conversación con IA.

    Returns:
        EnhancedAIConversationService: Instancia del servicio mejorado de conversación con IA
    """
    global _enhanced_ai_conversation_service
    if _enhanced_ai_conversation_service is None:
        _enhanced_ai_conversation_service = EnhancedAIConversationService()
    return _enhanced_ai_conversation_service


async def get_elevenlabs_service() -> ElevenLabsService:
    """
    Obtiene una instancia singleton del servicio de ElevenLabs.

    Returns:
        ElevenLabsService: Instancia del servicio de ElevenLabs
    """
    global _elevenlabs_service
    if _elevenlabs_service is None:
        _elevenlabs_service = ElevenLabsService()
    return _elevenlabs_service


async def get_audio_cache_service() -> AudioCacheService:
    """
    Obtiene una instancia singleton del servicio de caché de audio.

    Returns:
        AudioCacheService: Instancia del servicio de caché de audio
    """
    global _audio_cache_service
    if _audio_cache_service is None:
        _audio_cache_service = AudioCacheService()
    return _audio_cache_service


# Anotaciones para uso con Depends
CallServiceDep = Annotated[CallService, Depends(get_call_service)]
TwilioServiceDep = Annotated[TwilioService, Depends(get_twilio_service)]
CampaignServiceDep = Annotated[CampaignService, Depends(get_campaign_service)]
ContactServiceDep = Annotated[ContactService, Depends(get_contact_service)]
AIConversationServiceDep = Annotated[AIConversationService, Depends(get_ai_conversation_service)]
EnhancedAIConversationServiceDep = Annotated[
    EnhancedAIConversationService, Depends(get_enhanced_ai_conversation_service)
]
ElevenLabsServiceDep = Annotated[ElevenLabsService, Depends(get_elevenlabs_service)]
AudioCacheServiceDep = Annotated[AudioCacheService, Depends(get_audio_cache_service)]
