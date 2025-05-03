import os  # Importar os
from functools import lru_cache

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str

    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_KEY: str

    # Twilio Configuration
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str

    # Application Configuration
    APP_NAME: str
    APP_ENV: str = "development"
    APP_DEBUG: bool
    APP_URL: str

    # Security Configuration
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Server Configuration
    HOST: str
    PORT: int
    DEBUG: bool
    ENVIRONMENT: str

    # Scheduler Configuration
    SCHEDULER_CHECK_INTERVAL: int = 60  # Intervalo en segundos para revisar campañas
    SCHEDULER_MAX_CONCURRENT_CALLS: int = 10  # Máximo de llamadas simultáneas
    SCHEDULER_RETRY_DELAY: int = 15  # Tiempo en minutos entre reintentos por defecto
    SCHEDULER_DEFAULT_MAX_RETRIES: int = 3  # Número máximo de reintentos por defecto

    # Call Configuration
    CALL_TIMEOUT: int = 30  # Tiempo máximo de espera para una llamada en segundos
    CALL_DEFAULT_WEBHOOK_BASE_URL: str = ""  # URL base para webhooks de llamadas
    CALL_DEFAULT_FROM_NUMBER: str = ""  # Número de teléfono por defecto para realizar llamadas

    # ElevenLabs Configuration
    ELEVENLABS_API_KEY: str = Field(...)
    ELEVENLABS_DEFAULT_VOICE: str = "Bella"
    ELEVENLABS_MAX_RETRIES: int = 3
    ELEVENLABS_BACKOFF_FACTOR: float = 2
    ELEVENLABS_MAX_CONNECTIONS: int = 10
    ELEVENLABS_POOL_TIMEOUT: int = 30
    ELEVENLABS_CONNECTION_TIMEOUT: int = 30

    # Vault Configuration (Required for production)
    VAULT_ADDR: str = "http://vault:8200"
    VAULT_TOKEN_FILE: str = "/run/secrets/vault-token"
    VAULT_MOUNT_POINT: str = "kv"
    VAULT_PATH: str = "elevenlabs"

    # Metrics Configuration (Optional)
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090

    # Logging Configuration
    LOG_LEVEL: str = "info"
    LOG_FILE: str | None = "logs/app.log"
    LOG_FORMAT: str = "json"
    LOG_ROTATION: bool = True
    LOG_RETENTION_DAYS: int = 30

    # Audio Cache Configuration
    AUDIO_CACHE_ENABLED: bool = True
    AUDIO_CACHE_DIR: str = "cache/audio"
    AUDIO_CACHE_TTL: int = 86400  # 24 horas en segundos
    AUDIO_CACHE_MAX_SIZE: int = 1073741824  # 1 GB en bytes

    # Supabase Authentication Configuration
    SUPABASE_JWT_SECRET: str = os.getenv("SUPABASE_JWT_SECRET", "")
    AUTH_ENABLED: bool = os.getenv("AUTH_ENABLED", "true").lower() == "true"

    model_config = ConfigDict(
        # env_file=".env", # Se definirá dinámicamente en get_settings
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns cached settings instance, loading the appropriate .env file.
    """
    app_env = os.getenv("APP_ENV", "development")
    env_filename = f".env.{app_env}"

    # Si el archivo específico del entorno no existe, intenta cargar el .env por defecto
    if not os.path.exists(env_filename):
        env_filename = ".env"

    # Pasar _env_file explícitamente
    # Pydantic-settings buscará este archivo
    # Si env_filename tampoco existe, _env_file será None y pydantic-settings buscará variables de entorno
    return Settings(_env_file=env_filename if os.path.exists(env_filename) else None)


# Create a global settings instance
settings = get_settings()
