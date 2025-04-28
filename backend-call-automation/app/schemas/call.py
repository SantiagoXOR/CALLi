from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID
from app.models.call import CallStatus

class CallCreate(BaseModel):
    campaign_id: str = Field(..., description="ID de la campaña")
    phone_number: str = Field(..., description="Número de teléfono destino")
    from_number: str = Field(..., description="Número de teléfono origen")
    webhook_url: str = Field(..., description="URL para manejo de llamada")
    status_callback_url: str = Field(..., description="URL para actualizaciones de estado")
    timeout: int = Field(30, description="Tiempo máximo de espera en segundos")
    max_retries: int = Field(3, description="Máximo de intentos permitidos")
    script_template: str = Field(..., description="Texto para generación de audio")

    model_config = ConfigDict(from_attributes=True)

class CallUpdate(BaseModel):
    status: Optional[CallStatus] = Field(None, description="Estado actualizado de la llamada")
    duration: Optional[int] = Field(None, description="Duración en segundos")
    recording_url: Optional[str] = Field(None, description="URL de grabación")
    error_message: Optional[str] = Field(None, description="Mensaje de error si hubo fallo")
    retry_attempts: Optional[int] = Field(None, description="Número de intentos realizados")

    model_config = ConfigDict(from_attributes=True)
