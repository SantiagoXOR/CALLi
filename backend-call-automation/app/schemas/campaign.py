from datetime import datetime
from uuid import UUID
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, ConfigDict, validator
from app.models.campaign import CampaignStatus

class CampaignCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Nombre de la campaña")
    description: Optional[str] = Field(None, description="Descripción detallada")
    status: CampaignStatus = Field(
        default=CampaignStatus.DRAFT,
        description="Estado inicial de la campaña"
    )
    schedule_start: datetime = Field(..., description="Fecha y hora de inicio")
    schedule_end: datetime = Field(..., description="Fecha y hora de finalización")
    contact_list_ids: List[UUID] = Field(
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
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[CampaignStatus] = None
    schedule_start: Optional[datetime] = None
    schedule_end: Optional[datetime] = None
    contact_list_ids: Optional[List[UUID]] = None
    script_template: Optional[str] = Field(None, min_length=10)
    max_retries: Optional[int] = Field(None, ge=0)
    retry_delay_minutes: Optional[int] = Field(None, ge=0)
    calling_hours_start: Optional[str] = None
    calling_hours_end: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
