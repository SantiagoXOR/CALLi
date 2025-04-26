# Modelos de Datos

## Visión General

Este documento describe los modelos de datos utilizados en el sistema de automatización de llamadas. Los modelos están implementados utilizando Pydantic para la validación de datos y se utilizan tanto para la comunicación con la API como para la interacción con la base de datos.

## Modelo Base

Todos los modelos de base de datos heredan de `BaseDBModel`, que proporciona campos comunes:

```python
class BaseDBModel(BaseModel):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

## Modelos Principales

### Campaign (Campaña)

El modelo `Campaign` representa una campaña de llamadas automatizadas.

#### Enumeraciones

```python
class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
```

#### Modelos

```python
class CampaignBase(BaseModel):
    name: str
    description: str | None = None
    status: CampaignStatus = CampaignStatus.DRAFT
    schedule_start: datetime | None = None
    schedule_end: datetime | None = None
    script_template: str
    max_retries: int = 3
    retry_delay_minutes: int = 60
    calling_hours_start: time | None = None
    calling_hours_end: time | None = None

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: CampaignStatus | None = None
    schedule_start: datetime | None = None
    schedule_end: datetime | None = None
    script_template: str | None = None
    max_retries: int | None = None
    retry_delay_minutes: int | None = None
    calling_hours_start: time | None = None
    calling_hours_end: time | None = None

class Campaign(BaseDBModel, CampaignBase):
    pending_calls: int = 0
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
```

### Call (Llamada)

El modelo `Call` representa una llamada individual dentro de una campaña.

#### Enumeraciones

```python
class CallStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PENDING = "pending"
```

#### Modelos

```python
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

class CallCreate(CallBase):
    campaign_id: str = Field(..., description="ID de la campaña")
    phone_number: str = Field(..., description="Número destino")
    from_number: str = Field(..., description="Número origen")
    webhook_url: str = Field(..., description="URL para webhook")
    status_callback_url: str = Field(..., description="URL para callbacks")
    timeout: int = Field(30, description="Tiempo máximo de espera")
    max_retries: int = Field(3, description="Máximo de intentos")

class CallUpdate(BaseModel):
    status: CallStatus | None = None
    duration: int | None = None
    recording_url: str | None = None
    error_message: str | None = None
    retry_attempts: int | None = None

class Call(BaseDBModel, CallBase):
    campaign_id: UUID
    phone_number: str
    from_number: str
    error_message: str | None = None
```

### Contact (Contacto)

El modelo `Contact` representa un contacto al que se puede llamar.

```python
class ContactBase(BaseModel):
    name: str
    phone_number: constr(regex=r'^\+?1?\d{9,15}$')  # International phone number format
    email: Optional[EmailStr] = None
    notes: Optional[str] = None
    tags: list[str] = []

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    name: Optional[str] = None
    phone_number: Optional[str] = None

class Contact(BaseDBModel, ContactBase):
    pass
```

### User (Usuario)

El modelo `User` representa un usuario del sistema.

```python
class UserRole(str, Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    password: Optional[str] = None

class User(BaseDBModel, UserBase):
    pass
```

### CallMetrics (Métricas de Llamadas)

El modelo `CallMetrics` representa métricas agregadas de llamadas.

```python
class CallMetrics(BaseModel):
    total_calls: int = Field(default=0, description="Total de llamadas")
    completed_calls: int = Field(default=0, description="Llamadas completadas")
    failed_calls: int = Field(default=0, description="Llamadas fallidas")
    no_answer_calls: int = Field(default=0, description="Llamadas sin respuesta")
    busy_calls: int = Field(default=0, description="Llamadas ocupadas")
    avg_duration: float = Field(default=0.0, description="Duración promedio de las llamadas en segundos")
    
    model_config = ConfigDict(from_attributes=True)
```

## Relaciones entre Modelos

- Una **Campaign** puede tener múltiples **Calls**
- Un **Contact** puede estar asociado a múltiples **Calls**
- Un **Contact** puede pertenecer a múltiples **Campaigns** (a través de una tabla de unión)
- Un **User** puede crear y gestionar múltiples **Campaigns**

## Validación de Datos

Los modelos utilizan las capacidades de validación de Pydantic para garantizar la integridad de los datos:

- Validación de formato de número de teléfono mediante expresiones regulares
- Validación de formato de correo electrónico
- Valores predeterminados para campos opcionales
- Restricciones de tipos de datos

## Serialización y Deserialización

Los modelos Pydantic facilitan la serialización y deserialización de datos:

- Conversión automática entre objetos Python y JSON
- Manejo de fechas y horas en formato ISO
- Conversión de tipos de datos (por ejemplo, strings a enumeraciones)
- Validación de datos durante la deserialización
