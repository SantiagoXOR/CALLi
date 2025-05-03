"""
Modelos para la gestión de llamadas.
"""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CallStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PENDING = "pending"
    NO_ANSWER = "no_answer"
    BUSY = "busy"
    ERROR = "error"


class CallBase(BaseModel):
    contact_id: UUID = Field(..., description="ID del contacto")
    scheduled_time: datetime | None = Field(None, description="Fecha programada para la llamada")
    status: CallStatus = Field(..., description="Estado actual de la llamada")
    duration: int | None = Field(None, description="Duración en segundos")
    recording_url: str | None = Field(None, description="URL de grabación")
    notes: str | None = Field(None, description="Notas adicionales")
    twilio_sid: str | None = Field(None, description="SID de Twilio")
    retry_attempts: int = Field(0, description="Número de intentos")
    max_retries: int = Field(3, description="Máximo de intentos permitidos")
    script_template: str = Field(..., description="Texto para audio")
    webhook_url: str = Field(..., description="URL para webhook")
    status_callback_url: str = Field(..., description="URL para callbacks")
    phone_number: str = Field(..., description="Número destino")
    from_number: str = Field(..., description="Número origen")
    error_message: str | None = Field(None, description="Mensaje de error")

    model_config = ConfigDict(from_attributes=True)


class CallCreate(CallBase):
    campaign_id: str = Field(..., description="ID de la campaña")
    phone_number: str = Field(..., description="Número destino")
    from_number: str = Field(..., description="Número origen")
    webhook_url: str = Field(..., description="URL para webhook")
    status_callback_url: str = Field(..., description="URL para callbacks")
    timeout: int = Field(30, description="Tiempo máximo de espera")
    max_retries: int = Field(3, description="Máximo de intentos")

    model_config = ConfigDict(from_attributes=True)


class CallUpdate(BaseModel):
    status: CallStatus | None = None
    duration: int | None = None
    recording_url: str | None = None
    error_message: str | None = None
    retry_attempts: int | None = None

    model_config = ConfigDict(from_attributes=True)


class Call(CallBase):
    id: UUID = Field(..., description="ID único de la llamada")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de actualización")
    campaign_id: str = Field(..., description="ID de la campaña")
    interaction_history: list[dict[str, Any]] | None = Field(
        None, description="Historial de interacciones"
    )

    model_config = ConfigDict(from_attributes=True)


class InteractionItem(BaseModel):
    """Representa una interacción individual en una llamada."""

    timestamp: datetime = Field(..., description="Momento de la interacción")
    type: str = Field(..., description="Tipo de interacción (user, ai, system)")
    content: str = Field(..., description="Contenido de la interacción")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Metadatos adicionales")

    model_config = ConfigDict(from_attributes=True)


class CallDetail(BaseModel):
    """Modelo detallado de una llamada con información completa."""

    id: UUID = Field(..., description="ID único de la llamada")
    contact_id: UUID = Field(..., description="ID del contacto")
    campaign_id: str = Field(..., description="ID de la campaña")
    contact_name: str = Field(..., description="Nombre del contacto")
    contact_phone: str = Field(..., description="Teléfono del contacto")
    campaign_name: str = Field(..., description="Nombre de la campaña")
    status: CallStatus = Field(..., description="Estado actual de la llamada")
    scheduled_time: datetime | None = Field(None, description="Fecha programada")
    start_time: datetime | None = Field(None, description="Hora de inicio")
    end_time: datetime | None = Field(None, description="Hora de finalización")
    duration: int | None = Field(None, description="Duración en segundos")
    recording_url: str | None = Field(None, description="URL de grabación")
    notes: str | None = Field(None, description="Notas adicionales")
    twilio_sid: str | None = Field(None, description="SID de Twilio")
    retry_attempts: int = Field(0, description="Número de intentos")
    max_retries: int = Field(3, description="Máximo de intentos permitidos")
    error_message: str | None = Field(None, description="Mensaje de error")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de actualización")
    interactions: list[InteractionItem] = Field(
        default_factory=list, description="Historial de interacciones"
    )
    call_metrics: dict[str, Any] = Field(
        default_factory=dict, description="Métricas de la llamada (duración, silencios, etc.)"
    )
    tags: list[str] = Field(default_factory=list, description="Etiquetas de la llamada")

    model_config = ConfigDict(from_attributes=True)
