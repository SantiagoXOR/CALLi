# Servicio de Campañas

## Visión General

El `CampaignService` es un componente fundamental del sistema de automatización de llamadas que gestiona el ciclo de vida completo de las campañas de llamadas. Este servicio proporciona funcionalidades para crear, consultar, actualizar y eliminar campañas, así como para gestionar sus estadísticas y estado.

## Funcionalidades Principales

### 1. Gestión de Campañas

- **Crear campañas**: Crear nuevas campañas con configuración personalizada
- **Consultar campañas**: Obtener información detallada de campañas
- **Actualizar campañas**: Modificar configuración y estado de campañas
- **Eliminar campañas**: Eliminar campañas y sus datos asociados

### 2. Programación de Campañas

- **Programar inicio**: Configurar fecha y hora de inicio de campañas
- **Programar finalización**: Configurar fecha y hora de finalización de campañas
- **Gestionar horarios**: Definir horarios permitidos para realizar llamadas
- **Pausar y reanudar**: Controlar la ejecución de campañas

### 3. Estadísticas y Monitoreo

- **Estadísticas en tiempo real**: Proporcionar métricas actualizadas de campañas
- **Historial de campañas**: Mantener registro histórico de campañas
- **Análisis de rendimiento**: Calcular tasas de éxito y otros indicadores
- **Exportación de datos**: Generar informes y exportar datos

### 4. Gestión de Contactos

- **Asignar contactos**: Asociar contactos a campañas
- **Importar contactos**: Importar listas de contactos desde archivos
- **Segmentación**: Filtrar contactos según criterios específicos
- **Priorización**: Establecer prioridades para llamadas a contactos

## Implementación

### Clase Principal

```python
class CampaignService:
    """Servicio para gestionar campañas de llamadas automatizadas.
    
    Este servicio proporciona métodos para crear, consultar, actualizar y eliminar campañas,
    así como para gestionar sus estadísticas y estado.
    
    Attributes:
        supabase: Cliente de Supabase para la persistencia de datos
    """
    def __init__(self, supabase_client):
        """Inicializa el servicio de campañas.
        
        Args:
            supabase_client: Cliente de Supabase para la persistencia de datos
        """
        self.supabase = supabase_client
        self.table_name = "campaigns"
```

### Métodos Principales

#### Gestión de Campañas

```python
async def create_campaign(self, campaign: CampaignCreate) -> Campaign:
    """Crea una nueva campaña de llamadas.
    
    Args:
        campaign: Datos de la campaña a crear
        
    Returns:
        Campaign: La campaña creada con su ID asignado
        
    Raises:
        HTTPException: Si hay un error al crear la campaña
    """
    try:
        result = self.supabase.from_table(self.table_name).insert(campaign.model_dump()).execute()
        if result and result["data"]:
            return Campaign(**result["data"][0])
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear la campaña"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la campaña: {str(e)}"
        )

async def get_campaign(self, campaign_id: str) -> Campaign:
    """Obtiene una campaña por su ID.
    
    Args:
        campaign_id: ID de la campaña
        
    Returns:
        Campaign: La campaña encontrada
        
    Raises:
        HTTPException: Si la campaña no existe o hay un error
    """
    try:
        result = self.supabase.from_table(self.table_name).select("*").eq("id", campaign_id).execute()
        if not result or not result["data"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaña no encontrada"
            )
        return Campaign(**result["data"][0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la campaña: {str(e)}"
        )

async def update_campaign(self, campaign_id: str, campaign: CampaignUpdate) -> Campaign:
    """Actualiza una campaña existente.
    
    Args:
        campaign_id: ID de la campaña a actualizar
        campaign: Datos a actualizar
        
    Returns:
        Campaign: La campaña actualizada
        
    Raises:
        HTTPException: Si la campaña no existe o hay un error
    """
    try:
        # Filtrar campos None para no sobrescribir con valores nulos
        update_data = {k: v for k, v in campaign.model_dump().items() if v is not None}
        
        result = self.supabase.from_table(self.table_name).update(update_data).eq("id", campaign_id).execute()
        if not result or not result["data"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaña no encontrada"
            )
        return Campaign(**result["data"][0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la campaña: {str(e)}"
        )

async def delete_campaign(self, campaign_id: str) -> bool:
    """Elimina una campaña.
    
    Args:
        campaign_id: ID de la campaña a eliminar
        
    Returns:
        bool: True si se eliminó correctamente
        
    Raises:
        HTTPException: Si la campaña no existe o hay un error
    """
    try:
        result = self.supabase.from_table(self.table_name).delete().eq("id", campaign_id).execute()
        if not result or not result["data"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaña no encontrada"
            )
        return True
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la campaña: {str(e)}"
        )
```

#### Listado y Filtrado de Campañas

```python
async def list_campaigns(
    self, 
    status: Optional[CampaignStatus] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Campaign]:
    """Lista campañas con filtros opcionales.
    
    Args:
        status: Filtrar por estado (opcional)
        skip: Número de registros a omitir (paginación)
        limit: Número máximo de registros a devolver
        
    Returns:
        List[Campaign]: Lista de campañas
        
    Raises:
        HTTPException: Si hay un error al listar las campañas
    """
    try:
        query = self.supabase.from_table(self.table_name).select("*")
        
        if status:
            query = query.eq("status", status.value)
        
        query = query.range(skip, skip + limit - 1)
        
        result = query.execute()
        
        if not result:
            return []
        
        return [Campaign(**item) for item in result["data"]]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar campañas: {str(e)}"
        )

async def search_campaigns(self, search_term: str, limit: int = 10) -> List[Campaign]:
    """Busca campañas por nombre o descripción.
    
    Args:
        search_term: Término de búsqueda
        limit: Número máximo de resultados
        
    Returns:
        List[Campaign]: Lista de campañas que coinciden con la búsqueda
        
    Raises:
        HTTPException: Si hay un error en la búsqueda
    """
    try:
        # Búsqueda en nombre (más relevante)
        name_query = self.supabase.from_table(self.table_name).select("*").ilike("name", f"%{search_term}%").limit(limit)
        name_result = name_query.execute()
        
        # Si no hay suficientes resultados, buscar también en descripción
        if not name_result or len(name_result["data"]) < limit:
            remaining = limit - (len(name_result["data"]) if name_result and name_result["data"] else 0)
            desc_query = self.supabase.from_table(self.table_name).select("*").ilike("description", f"%{search_term}%").limit(remaining)
            desc_result = desc_query.execute()
            
            # Combinar resultados
            all_results = []
            if name_result and name_result["data"]:
                all_results.extend(name_result["data"])
            if desc_result and desc_result["data"]:
                all_results.extend(desc_result["data"])
                
            # Eliminar duplicados
            seen_ids = set()
            unique_results = []
            for item in all_results:
                if item["id"] not in seen_ids:
                    seen_ids.add(item["id"])
                    unique_results.append(item)
                    
            return [Campaign(**item) for item in unique_results]
        
        return [Campaign(**item) for item in name_result["data"]]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar campañas: {str(e)}"
        )
```

#### Gestión de Estado y Estadísticas

```python
async def update_campaign_status(self, campaign_id: str, status: CampaignStatus) -> Campaign:
    """Actualiza el estado de una campaña.
    
    Args:
        campaign_id: ID de la campaña
        status: Nuevo estado
        
    Returns:
        Campaign: La campaña actualizada
        
    Raises:
        HTTPException: Si la campaña no existe o hay un error
    """
    return await self.update_campaign(campaign_id, CampaignUpdate(status=status))

async def increment_successful_calls(self, campaign_id: str) -> Campaign:
    """Incrementa el contador de llamadas exitosas de una campaña.
    
    Args:
        campaign_id: ID de la campaña
        
    Returns:
        Campaign: La campaña actualizada
        
    Raises:
        HTTPException: Si la campaña no existe o hay un error
    """
    try:
        # Obtener campaña actual
        campaign = await self.get_campaign(campaign_id)
        
        # Incrementar contador y decrementar pendientes
        successful_calls = campaign.successful_calls + 1
        pending_calls = max(0, campaign.pending_calls - 1)
        
        # Actualizar campaña
        return await self.update_campaign(
            campaign_id,
            CampaignUpdate(
                successful_calls=successful_calls,
                pending_calls=pending_calls
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al incrementar llamadas exitosas: {str(e)}"
        )

async def increment_failed_calls(self, campaign_id: str) -> Campaign:
    """Incrementa el contador de llamadas fallidas de una campaña.
    
    Args:
        campaign_id: ID de la campaña
        
    Returns:
        Campaign: La campaña actualizada
        
    Raises:
        HTTPException: Si la campaña no existe o hay un error
    """
    try:
        # Obtener campaña actual
        campaign = await self.get_campaign(campaign_id)
        
        # Incrementar contador y decrementar pendientes
        failed_calls = campaign.failed_calls + 1
        pending_calls = max(0, campaign.pending_calls - 1)
        
        # Actualizar campaña
        return await self.update_campaign(
            campaign_id,
            CampaignUpdate(
                failed_calls=failed_calls,
                pending_calls=pending_calls
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al incrementar llamadas fallidas: {str(e)}"
        )

async def increment_pending_calls(self, campaign_id: str) -> Campaign:
    """Incrementa el contador de llamadas pendientes de una campaña.
    
    Args:
        campaign_id: ID de la campaña
        
    Returns:
        Campaign: La campaña actualizada
        
    Raises:
        HTTPException: Si la campaña no existe o hay un error
    """
    try:
        # Obtener campaña actual
        campaign = await self.get_campaign(campaign_id)
        
        # Incrementar contador
        pending_calls = campaign.pending_calls + 1
        total_calls = campaign.total_calls + 1
        
        # Actualizar campaña
        return await self.update_campaign(
            campaign_id,
            CampaignUpdate(
                pending_calls=pending_calls,
                total_calls=total_calls
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al incrementar llamadas pendientes: {str(e)}"
        )
```

#### Gestión de Contactos en Campañas

```python
async def add_contacts_to_campaign(self, campaign_id: str, contact_ids: List[str]) -> int:
    """Añade contactos a una campaña.
    
    Args:
        campaign_id: ID de la campaña
        contact_ids: Lista de IDs de contactos
        
    Returns:
        int: Número de contactos añadidos
        
    Raises:
        HTTPException: Si la campaña no existe o hay un error
    """
    try:
        # Verificar que la campaña existe
        await self.get_campaign(campaign_id)
        
        # Preparar datos para inserción
        now = datetime.now().isoformat()
        data = [
            {
                "campaign_id": campaign_id,
                "contact_id": contact_id,
                "call_status": "pending",
                "call_count": 0,
                "created_at": now,
                "updated_at": now
            }
            for contact_id in contact_ids
        ]
        
        # Insertar en tabla de relación
        result = self.supabase.from_table("campaign_contacts").insert(data).execute()
        
        if not result or not result["data"]:
            return 0
            
        # Actualizar contador de llamadas pendientes
        await self.update_campaign(
            campaign_id,
            CampaignUpdate(
                pending_calls=len(contact_ids),
                total_calls=len(contact_ids)
            )
        )
        
        return len(result["data"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al añadir contactos: {str(e)}"
        )

async def remove_contact_from_campaign(self, campaign_id: str, contact_id: str) -> bool:
    """Elimina un contacto de una campaña.
    
    Args:
        campaign_id: ID de la campaña
        contact_id: ID del contacto
        
    Returns:
        bool: True si se eliminó correctamente
        
    Raises:
        HTTPException: Si la relación no existe o hay un error
    """
    try:
        result = self.supabase.from_table("campaign_contacts").delete().eq("campaign_id", campaign_id).eq("contact_id", contact_id).execute()
        
        if not result or not result["data"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contacto no encontrado en la campaña"
            )
            
        return True
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar contacto: {str(e)}"
        )

async def get_campaign_contacts(self, campaign_id: str, skip: int = 0, limit: int = 100) -> List[Dict]:
    """Obtiene los contactos de una campaña.
    
    Args:
        campaign_id: ID de la campaña
        skip: Número de registros a omitir (paginación)
        limit: Número máximo de registros a devolver
        
    Returns:
        List[Dict]: Lista de contactos con su estado en la campaña
        
    Raises:
        HTTPException: Si la campaña no existe o hay un error
    """
    try:
        # Verificar que la campaña existe
        await self.get_campaign(campaign_id)
        
        # Consultar contactos de la campaña
        query = self.supabase.from_table("campaign_contacts").select("*, contacts(*)").eq("campaign_id", campaign_id).range(skip, skip + limit - 1)
        result = query.execute()
        
        if not result or not result["data"]:
            return []
            
        # Formatear resultados
        contacts = []
        for item in result["data"]:
            contact_data = item["contacts"]
            contact_data["call_status"] = item["call_status"]
            contact_data["call_count"] = item["call_count"]
            contact_data["last_call_at"] = item["last_call_at"]
            contacts.append(contact_data)
            
        return contacts
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener contactos: {str(e)}"
        )
```

## Configuración

El servicio de campañas no requiere configuración específica más allá del cliente de Supabase que se inyecta en el constructor.

## Uso

### Inicialización

```python
# En app/main.py
from app.services.campaign_service import CampaignService
from app.config.supabase import supabase_client

campaign_service = CampaignService(supabase_client=supabase_client)
```

### Uso en Endpoints

```python
# En app/routers/campaigns.py
@router.post("/", response_model=Campaign)
async def create_campaign(campaign: CampaignCreate):
    """Crea una nueva campaña."""
    return await campaign_service.create_campaign(campaign)

@router.get("/{campaign_id}", response_model=Campaign)
async def get_campaign(campaign_id: str):
    """Obtiene una campaña por su ID."""
    return await campaign_service.get_campaign(campaign_id)

@router.put("/{campaign_id}", response_model=Campaign)
async def update_campaign(campaign_id: str, campaign: CampaignUpdate):
    """Actualiza una campaña existente."""
    return await campaign_service.update_campaign(campaign_id, campaign)

@router.delete("/{campaign_id}", response_model=bool)
async def delete_campaign(campaign_id: str):
    """Elimina una campaña."""
    return await campaign_service.delete_campaign(campaign_id)

@router.get("/", response_model=List[Campaign])
async def list_campaigns(
    status: Optional[CampaignStatus] = None,
    skip: int = 0,
    limit: int = 100
):
    """Lista campañas con filtros opcionales."""
    return await campaign_service.list_campaigns(status, skip, limit)

@router.post("/{campaign_id}/status", response_model=Campaign)
async def update_status(campaign_id: str, status: CampaignStatus):
    """Actualiza el estado de una campaña."""
    return await campaign_service.update_campaign_status(campaign_id, status)

@router.post("/{campaign_id}/contacts", response_model=int)
async def add_contacts(campaign_id: str, contact_ids: List[str]):
    """Añade contactos a una campaña."""
    return await campaign_service.add_contacts_to_campaign(campaign_id, contact_ids)

@router.get("/{campaign_id}/contacts", response_model=List[Dict])
async def get_contacts(campaign_id: str, skip: int = 0, limit: int = 100):
    """Obtiene los contactos de una campaña."""
    return await campaign_service.get_campaign_contacts(campaign_id, skip, limit)
```

## Flujo de Trabajo de Campañas

1. **Creación**: Se crea una nueva campaña con `create_campaign`
2. **Configuración**: Se actualiza la configuración con `update_campaign`
3. **Asignación de contactos**: Se añaden contactos con `add_contacts_to_campaign`
4. **Activación**: Se cambia el estado a "active" con `update_campaign_status`
5. **Monitoreo**: Se consultan estadísticas periódicamente
6. **Finalización**: Se cambia el estado a "completed" cuando finaliza

## Consideraciones de Rendimiento

- **Paginación**: Implementación de paginación para grandes conjuntos de datos
- **Índices**: Uso de índices en la base de datos para consultas frecuentes
- **Caché**: Posibilidad de implementar caché para campañas frecuentemente accedidas
- **Consultas optimizadas**: Minimizar el número de consultas a la base de datos
- **Transacciones**: Uso de transacciones para operaciones que afectan a múltiples tablas

## Consideraciones de Seguridad

- **Validación de entrada**: Validación de todos los datos de entrada
- **Control de acceso**: Implementación de políticas de acceso basadas en roles
- **Auditoría**: Registro de cambios importantes en campañas
- **Sanitización de datos**: Limpieza de datos antes de procesarlos
- **Protección contra inyección SQL**: Uso de parámetros en consultas

## Solución de Problemas

### Problemas Comunes

1. **Campañas que no se activan**:
   - Verificar estado de la campaña
   - Comprobar fechas de inicio y fin
   - Verificar que hay contactos asignados

2. **Estadísticas incorrectas**:
   - Verificar contadores de llamadas
   - Comprobar sincronización entre tablas
   - Revisar logs para errores específicos

3. **Problemas de rendimiento**:
   - Monitorear tiempos de respuesta
   - Verificar índices en la base de datos
   - Optimizar consultas complejas

4. **Errores de permisos**:
   - Verificar políticas de seguridad en Supabase
   - Comprobar roles y permisos
   - Revisar logs para errores específicos

### Comandos Útiles

```bash
# Verificar logs
tail -f logs/campaign_service.log

# Consultar campañas activas
curl http://localhost:8000/api/v1/campaigns?status=active

# Obtener estadísticas de una campaña
curl http://localhost:8000/api/v1/campaigns/{campaign_id}
```

## Referencias

- [Supabase Documentation](https://supabase.io/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
