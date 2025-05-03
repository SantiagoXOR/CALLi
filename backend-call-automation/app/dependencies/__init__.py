"""
Módulo de dependencias para la inyección de dependencias en FastAPI.
"""

# Importar las dependencias de servicio para que estén disponibles al importar app.dependencies
from app.dependencies.service_dependencies import (
    AIConversationServiceDep,
    AudioCacheServiceDep,
    CallServiceDep,
    CampaignServiceDep,
    ContactServiceDep,
    ElevenLabsServiceDep,
    EnhancedAIConversationServiceDep,
    TwilioServiceDep,
    get_ai_conversation_service,
    get_audio_cache_service,
    get_call_service,
    get_campaign_service,
    get_contact_service,
    get_elevenlabs_service,
    get_enhanced_ai_conversation_service,
    get_twilio_service,
)

__all__ = [
    "AIConversationServiceDep",
    "AudioCacheServiceDep",
    "CallServiceDep",
    "CampaignServiceDep",
    "ContactServiceDep",
    "ElevenLabsServiceDep",
    "EnhancedAIConversationServiceDep",
    "TwilioServiceDep",
    "get_ai_conversation_service",
    "get_audio_cache_service",
    "get_call_service",
    "get_campaign_service",
    "get_contact_service",
    "get_elevenlabs_service",
    "get_enhanced_ai_conversation_service",
    "get_twilio_service",
]
