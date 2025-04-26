from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, validator
from app.models.campaign import CampaignStatus

class CampaignCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Nombre de la campaña")
    description: str | None = Field(None, description="Descripción detallada")
    status: CampaignStatus = Field(
        default=CampaignStatus.DRAFT,
        description="Estado inicial de la campaña"
    )
    schedule_start: datetime = Field(..., description="Fecha y hora de inicio")
    schedule_end: datetime = Field(..., description="Fecha y hora de finalización")
    contact_list_ids: list[UUID] = Field(
        default_factory=list,
        description="IDs de listas de contactos"
    )
    script_template: str = Field(..., min_length=10, description="Plantilla del script")
    max_retries: int = Field(default=3, ge=0, description="Máximo de reintentos")
    retry_delay_minutes: int = Field(default=60, ge=0, description="Tiempo entre reintentos (min)")
    calling_hours_start: str = Field(..., description="Hora inicio llamadas (HH:MM)")
    calling_hours_end: str = Field(..., description="Hora fin llamadas (HH:MM)")

    model_config = ConfigDict(from_attributes=True)

    @validator("schedule_end")
    def validate_schedule_end(cls, v: datetime, values: dict) -> datetime:
        if "schedule_start" in values and v <= values["schedule_start"]:
            raise ValueError("La fecha de fin debe ser posterior a la de inicio")
        return v

    @validator("calling_hours_end")
    def validate_calling_hours(cls, v: str, values: dict) -> str:
        if "calling_hours_start" in values:
            start = datetime.strptime(values["calling_hours_start"], "%H:%M").time()
            end = datetime.strptime(v, "%H:%M").time()
            if end <= start:
                raise ValueError("La hora de fin debe ser posterior a la de inicio")
        return v

class CampaignUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    status: CampaignStatus | None = None
    schedule_start: datetime | None = None
    schedule_end: datetime | None = None
    contact_list_ids: list[UUID] | None = None
    script_template: str | None = Field(None, min_length=10)
    max_retries: int | None = Field(None, ge=0)
    retry_delay_minutes: int | None = Field(None, ge=0)
    calling_hours_start: str | None = None
    calling_hours_end: str | None = None

    model_config = ConfigDict(from_attributes=True)
