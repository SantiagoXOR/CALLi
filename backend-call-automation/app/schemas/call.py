from pydantic import BaseModel, ConfigDict, Field

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
    status: CallStatus | None = Field(None, description="Estado actualizado de la llamada")
    duration: int | None = Field(None, description="Duración en segundos")
    recording_url: str | None = Field(None, description="URL de grabación")
    error_message: str | None = Field(None, description="Mensaje de error si hubo fallo")
    retry_attempts: int | None = Field(None, description="Número de intentos realizados")

    model_config = ConfigDict(from_attributes=True)
