"""
Modelo para las métricas de llamadas.
"""
from pydantic import BaseModel, Field, ConfigDict

class CallMetrics(BaseModel):
    """
    Modelo que representa las métricas de llamadas.
    """
    total_calls: int = Field(default=0, description="Total de llamadas")
    completed_calls: int = Field(default=0, description="Llamadas completadas")
    failed_calls: int = Field(default=0, description="Llamadas fallidas")
    no_answer_calls: int = Field(default=0, description="Llamadas sin respuesta")
    busy_calls: int = Field(default=0, description="Llamadas ocupadas")
    avg_duration: float = Field(default=0.0, description="Duración promedio de las llamadas en segundos")
    
    model_config = ConfigDict(from_attributes=True)
