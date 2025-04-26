from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, field_validator

class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class CampaignType(str, Enum):
    SALES = "sales"
    SUPPORT = "support"
    SURVEY = "survey"
    FOLLOW_UP = "follow_up"
    EDUCATIONAL = "educational"
    RETENTION = "retention"

class AIConfig(BaseModel):
    """Configuración específica para la IA en una campaña."""
    model: str = Field(default="gpt-4", description="Modelo de IA a utilizar")
    temperature: float = Field(default=0.7, ge=0, le=1, description="Temperatura para la generación")
    max_tokens: int = Field(default=150, ge=0, description="Máximo de tokens por respuesta")
    custom_prompt_variables: Dict[str, str] = Field(
        default_factory=dict,
        description="Variables personalizadas para el prompt"
    )

    model_config = ConfigDict(from_attributes=True)

class CampaignBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Nombre de la campaña")
    description: Optional[str] = Field(None, description="Descripción detallada de la campaña")
    status: CampaignStatus = Field(
        default=CampaignStatus.DRAFT,
        description="Estado actual de la campaña"
    )
    campaign_type: CampaignType = Field(
        default=CampaignType.SALES,
        description="Tipo de campaña que determina el comportamiento de la IA"
    )
    schedule_start: datetime = Field(..., description="Fecha y hora de inicio")
    schedule_end: datetime = Field(..., description="Fecha y hora de finalización")
    contact_list_ids: List[UUID] = Field(
        default_factory=list,
        description="Lista de IDs de contactos objetivo"
    )
    script_template: str = Field(..., min_length=10, description="Plantilla para el script de llamada")
    max_retries: int = Field(default=3, ge=0, description="Número máximo de reintentos por llamada")
    retry_delay_minutes: int = Field(
        default=60,
        ge=0,
        description="Tiempo de espera entre reintentos en minutos"
    )
    calling_hours_start: str = Field(..., description="Hora de inicio de llamadas (HH:MM)")
    calling_hours_end: str = Field(..., description="Hora de fin de llamadas (HH:MM)")
    pending_calls: int = Field(default=0, ge=0, description="Número de llamadas pendientes")
    ai_config: AIConfig = Field(
        default_factory=AIConfig,
        description="Configuración específica para la IA"
    )
    key_points: List[str] = Field(
        default_factory=list,
        description="Puntos clave a mencionar durante la llamada"
    )

    model_config = ConfigDict(from_attributes=True)

    @field_validator("schedule_end")
    def end_must_be_after_start(cls, v: datetime, info) -> datetime:
        if "schedule_start" in info.data and v <= info.data["schedule_start"]:
            raise ValueError("La fecha de finalización debe ser posterior a la de inicio")
        return v

    @field_validator("calling_hours_end")
    def validate_calling_hours(cls, v: str, info) -> str:
        if "calling_hours_start" in info.data:
            start = datetime.strptime(info.data["calling_hours_start"], "%H:%M").time()
            end = datetime.strptime(v, "%H:%M").time()
            if end <= start:
                raise ValueError("La hora de fin debe ser posterior a la de inicio")
        return v

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[CampaignStatus] = None
    campaign_type: Optional[CampaignType] = None
    schedule_start: Optional[datetime] = None
    schedule_end: Optional[datetime] = None
    contact_list_ids: Optional[List[UUID]] = None
    script_template: Optional[str] = Field(None, min_length=10)
    max_retries: Optional[int] = Field(None, ge=0)
    retry_delay_minutes: Optional[int] = Field(None, ge=0)
    calling_hours_start: Optional[str] = None
    calling_hours_end: Optional[str] = None
    pending_calls: Optional[int] = Field(None, ge=0)
    ai_config: Optional[AIConfig] = None
    key_points: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)

class CampaignStats(BaseModel):
    """Estadísticas de una campaña para actualización."""
    total_calls: int = Field(..., ge=0, description="Total de llamadas realizadas")
    successful_calls: int = Field(..., ge=0, description="Llamadas exitosas")
    failed_calls: int = Field(..., ge=0, description="Llamadas fallidas")
    pending_calls: int = Field(..., ge=0, description="Llamadas pendientes")

    model_config = ConfigDict(from_attributes=True)

    @field_validator("successful_calls", "failed_calls")
    def validate_call_counts(cls, v: int, info) -> int:
        if "total_calls" in info.data and "successful_calls" in info.data and "failed_calls" in info.data:
            total = info.data["total_calls"]
            successful = info.data["successful_calls"]
            failed = info.data["failed_calls"]

            # Validar que la suma de exitosas y fallidas no exceda el total
            if successful + failed > total:
                raise ValueError("La suma de llamadas exitosas y fallidas no puede exceder el total")
        return v

class Campaign(CampaignBase):
    id: UUID = Field(..., description="ID único de la campaña")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Última actualización")
    total_calls: int = Field(default=0, ge=0, description="Total de llamadas realizadas")
    successful_calls: int = Field(default=0, ge=0, description="Llamadas exitosas")
    failed_calls: int = Field(default=0, ge=0, description="Llamadas fallidas")

    model_config = ConfigDict(from_attributes=True)
