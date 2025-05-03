# Integración con Supabase

## Visión General

El sistema de automatización de llamadas utiliza [Supabase](https://supabase.io/) como plataforma de base de datos y autenticación. Supabase proporciona una capa de abstracción sobre PostgreSQL, junto con funcionalidades adicionales como autenticación, almacenamiento y funciones en tiempo real.

## Configuración

### Variables de Entorno

La configuración de Supabase se realiza a través de variables de entorno:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
```

### Cliente de Supabase

El cliente de Supabase se configura en el módulo `app/config/supabase.py`:

```python
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables")

supabase_client: Client = create_client(supabase_url, supabase_key)
```

## Migraciones de Base de Datos

Las migraciones de base de datos se gestionan a través de archivos SQL en el directorio `supabase/migrations/`. Estos archivos se ejecutan en orden secuencial para crear y actualizar el esquema de la base de datos.

### Ejemplo de Migración Inicial

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create campaigns table
create table if not exists campaigns (
    id uuid primary key default uuid_generate_v4(),
    name varchar(255) not null,
    description text,
    status campaign_status default 'draft',
    schedule_start timestamp with time zone,
    schedule_end timestamp with time zone,
    script_template text,
    max_retries integer default 3,
    retry_delay_minutes integer default 60,
    total_calls integer default 0,
    successful_calls integer default 0,
    failed_calls integer default 0,
    pending_calls integer default 0,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- Create contacts table
create table if not exists contacts (
    id uuid primary key default uuid_generate_v4(),
    phone_number varchar(20) not null,
    name varchar(255),
    email varchar(255),
    additional_data jsonb default '{}',
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- Create calls table
create table if not exists calls (
    id uuid primary key default uuid_generate_v4(),
    campaign_id uuid references campaigns(id) on delete cascade,
    contact_id uuid references contacts(id) on delete cascade,
    status call_status default 'pending',
    duration_seconds integer,
    attempt_count integer default 0,
    last_attempt_at timestamp with time zone,
    next_attempt_at timestamp with time zone,
    notes text,
    recording_url text,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);
```

## Operaciones CRUD

### Consulta de Datos

```python
async def get_campaign(campaign_id: str) -> Campaign:
    """Obtiene una campaña por su ID."""
    response = supabase_client.table("campaigns").select("*").eq("id", campaign_id).execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Campaign not found")

    return Campaign.model_validate(response.data[0])
```

### Inserción de Datos

```python
async def create_campaign(campaign: CampaignCreate) -> Campaign:
    """Crea una nueva campaña."""
    response = supabase_client.table("campaigns").insert(campaign.model_dump()).execute()

    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to create campaign")

    return Campaign.model_validate(response.data[0])
```

### Actualización de Datos

```python
async def update_campaign(campaign_id: str, campaign: CampaignUpdate) -> Campaign:
    """Actualiza una campaña existente."""
    # Filtrar campos None para no sobrescribir con valores nulos
    update_data = {k: v for k, v in campaign.model_dump().items() if v is not None}

    response = supabase_client.table("campaigns").update(update_data).eq("id", campaign_id).execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Campaign not found")

    return Campaign.model_validate(response.data[0])
```

### Eliminación de Datos

```python
async def delete_campaign(campaign_id: str) -> bool:
    """Elimina una campaña."""
    response = supabase_client.table("campaigns").delete().eq("id", campaign_id).execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Campaign not found")

    return True
```

## Consultas Avanzadas

### Filtrado

```python
async def get_campaigns_by_status(status: CampaignStatus) -> list[Campaign]:
    """Obtiene campañas por estado."""
    response = supabase_client.table("campaigns").select("*").eq("status", status).execute()

    return [Campaign.model_validate(item) for item in response.data]
```

### Ordenamiento

```python
async def get_recent_campaigns(limit: int = 10) -> list[Campaign]:
    """Obtiene las campañas más recientes."""
    response = supabase_client.table("campaigns").select("*").order("created_at", desc=True).limit(limit).execute()

    return [Campaign.model_validate(item) for item in response.data]
```

### Paginación

```python
async def get_campaigns_paginated(page: int = 1, page_size: int = 20) -> list[Campaign]:
    """Obtiene campañas con paginación."""
    offset = (page - 1) * page_size

    response = supabase_client.table("campaigns").select("*").range(offset, offset + page_size - 1).execute()

    return [Campaign.model_validate(item) for item in response.data]
```

### Joins

```python
async def get_campaign_with_calls(campaign_id: str) -> dict:
    """Obtiene una campaña con sus llamadas."""
    campaign_response = supabase_client.table("campaigns").select("*").eq("id", campaign_id).execute()

    if not campaign_response.data:
        raise HTTPException(status_code=404, detail="Campaign not found")

    calls_response = supabase_client.table("calls").select("*").eq("campaign_id", campaign_id).execute()

    return {
        "campaign": Campaign.model_validate(campaign_response.data[0]),
        "calls": [Call.model_validate(item) for item in calls_response.data]
    }
```

## Funciones RPC

Supabase permite definir funciones PostgreSQL que pueden ser llamadas a través de la API:

```sql
-- Función para obtener estadísticas de campaña
create or replace function get_campaign_stats(campaign_id uuid)
returns json as $$
declare
    result json;
begin
    select json_build_object(
        'total_calls', count(*),
        'completed_calls', count(*) filter (where status = 'completed'),
        'failed_calls', count(*) filter (where status = 'failed'),
        'pending_calls', count(*) filter (where status = 'pending'),
        'avg_duration', avg(duration_seconds) filter (where status = 'completed')
    )
    into result
    from calls
    where campaign_id = $1;

    return result;
end;
$$ language plpgsql;
```

Llamada desde Python:

```python
async def get_campaign_stats(campaign_id: str) -> dict:
    """Obtiene estadísticas de una campaña."""
    response = supabase_client.rpc("get_campaign_stats", {"campaign_id": campaign_id}).execute()

    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to get campaign stats")

    return response.data
```

## Políticas de Seguridad

Supabase permite definir políticas de seguridad a nivel de tabla para controlar el acceso a los datos:

```sql
-- Política para que los usuarios solo puedan ver sus propias campañas
create policy "Users can view their own campaigns"
on campaigns for select
using (auth.uid() = user_id);

-- Política para que los administradores puedan ver todas las campañas
create policy "Admins can view all campaigns"
on campaigns for select
using (
    exists (
        select 1 from users
        where users.id = auth.uid()
        and users.role = 'admin'
    )
);
```

## Suscripciones en Tiempo Real

Supabase proporciona capacidades de suscripción en tiempo real a través de WebSockets:

```python
# Ejemplo de suscripción a cambios en llamadas
subscription = supabase_client
    .table("calls")
    .on("INSERT", handle_new_call)
    .on("UPDATE", handle_call_update)
    .subscribe()

def handle_new_call(payload):
    print(f"New call: {payload}")

def handle_call_update(payload):
    print(f"Call updated: {payload}")
```

## Mejores Prácticas

1. **Utilizar transacciones** para operaciones que afectan a múltiples tablas
2. **Implementar políticas de seguridad** a nivel de base de datos
3. **Utilizar migraciones** para gestionar cambios en el esquema
4. **Validar datos** antes de enviarlos a Supabase
5. **Manejar errores** de forma adecuada
6. **Utilizar índices** para optimizar consultas frecuentes
7. **Limitar el número de conexiones** para evitar sobrecargar el servicio
8. **Implementar caché** para reducir el número de consultas
