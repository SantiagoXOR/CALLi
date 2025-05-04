from pydantic_settings import BaseSettings

# Importar los prompts optimizados
from app.config.campaign_prompts import CAMPAIGN_PROMPTS, DEFAULT_VALUES, REQUIRED_VARIABLES


class AISettings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str = "test_openai_api_key"
    GOOGLE_API_KEY: str = "AIzaSyBcDBONCgzY1i5LgXbVPcyehUkiAzO9yhE"
    ELEVENLABS_API_KEY: str = "test_elevenlabs_api_key"

    # Configuración de modelos
    LLM_PROVIDER: str = "google"  # "openai" o "google"
    DEFAULT_MODEL: str = "gpt-4"
    GOOGLE_MODEL: str = "gemini-pro"
    MAX_TOKENS: int = 150
    TEMPERATURE: float = 0.7

    # Configuración de voz
    ELEVENLABS_DEFAULT_VOICE: str = "Bella"

    # Configuración de memoria
    MAX_HISTORY_TOKENS: int = 2000
    MEMORY_TTL: int = 86400  # 24 horas

    # Prompts predefinidos por tipo de campaña
    CAMPAIGN_PROMPTS: dict[str, str] = CAMPAIGN_PROMPTS

    # Variables requeridas por tipo de campaña
    REQUIRED_VARIABLES: dict[str, list[str]] = REQUIRED_VARIABLES

    # Valores por defecto para variables opcionales
    DEFAULT_VALUES: dict[str, str] = DEFAULT_VALUES

    # Configuración de caché
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600  # 1 hora

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
