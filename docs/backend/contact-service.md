# Servicio de Contactos

## Visión General

El `ContactService` es un componente esencial del sistema de automatización de llamadas que gestiona la información de contactos y listas de contactos. Este servicio proporciona funcionalidades para crear, consultar, actualizar y eliminar contactos, así como para gestionar listas de contactos y asignarlos a campañas.

## Funcionalidades Principales

### 1. Gestión de Contactos

- **Crear contactos**: Añadir nuevos contactos al sistema
- **Consultar contactos**: Obtener información detallada de contactos
- **Actualizar contactos**: Modificar información de contactos existentes
- **Eliminar contactos**: Eliminar contactos del sistema

### 2. Gestión de Listas de Contactos

- **Crear listas**: Crear nuevas listas de contactos
- **Asignar contactos**: Añadir contactos a listas
- **Consultar listas**: Obtener información de listas y sus contactos
- **Eliminar listas**: Eliminar listas de contactos

### 3. Importación y Exportación

- **Importar contactos**: Importar contactos desde archivos CSV/Excel
- **Exportar contactos**: Exportar contactos a diferentes formatos
- **Validación de datos**: Validar información de contactos durante la importación
- **Gestión de errores**: Manejar errores durante la importación/exportación

### 4. Búsqueda y Filtrado

- **Búsqueda de contactos**: Buscar contactos por diferentes criterios
- **Filtrado avanzado**: Filtrar contactos por múltiples parámetros
- **Paginación**: Gestionar grandes conjuntos de datos
- **Ordenamiento**: Ordenar resultados según diferentes criterios

## Implementación

### Clase Principal

```python
class ContactService:
    """
    Servicio para gestionar operaciones relacionadas con contactos.

    Este servicio proporciona métodos para crear, actualizar, eliminar y listar
    contactos, así como gestionar listas de contactos y sus asignaciones a campañas.

    Attributes:
        None

    Dependencies:
        - supabase_client: Cliente de Supabase para operaciones de base de datos
    """

    def __init__(self, supabase_client=None):
        """
        Inicializa el servicio de contactos.

        Args:
            supabase_client: Cliente de Supabase para operaciones de base de datos
        """
        self.supabase = supabase_client or supabase_client
```

### Métodos Principales

#### Gestión de Contactos

```python
async def create_contact(self, contact: ContactCreate) -> Contact:
    """
    Crea un nuevo contacto.

    Args:
        contact: Datos del contacto a crear

    Returns:
        Contact: El contacto creado

    Raises:
        HTTPException: Si hay un error al crear el contacto
    """
    try:
        result = self.supabase.table('contacts').insert(contact.model_dump()).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear el contacto"
            )

        return Contact(**result.data[0])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el contacto: {str(e)}"
        )

async def get_contact(self, contact_id: str) -> Contact:
    """
    Obtiene un contacto por su ID.

    Args:
        contact_id: ID del contacto

    Returns:
        Contact: El contacto encontrado

    Raises:
        HTTPException: Si el contacto no existe o hay un error
    """
    try:
        result = self.supabase.table('contacts').select('*').eq('id', contact_id).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contacto no encontrado"
            )

        return Contact(**result.data[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el contacto: {str(e)}"
        )

async def update_contact(self, contact_id: str, contact: ContactUpdate) -> Contact:
    """
    Actualiza un contacto existente.

    Args:
        contact_id: ID del contacto a actualizar
        contact: Datos a actualizar

    Returns:
        Contact: El contacto actualizado

    Raises:
        HTTPException: Si el contacto no existe o hay un error
    """
    try:
        # Filtrar campos None para no sobrescribir con valores nulos
        update_data = {k: v for k, v in contact.model_dump().items() if v is not None}

        result = self.supabase.table('contacts').update(update_data).eq('id', contact_id).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contacto no encontrado"
            )

        return Contact(**result.data[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el contacto: {str(e)}"
        )

async def delete_contact(self, contact_id: str) -> bool:
    """
    Elimina un contacto.

    Args:
        contact_id: ID del contacto a eliminar

    Returns:
        bool: True si se eliminó correctamente

    Raises:
        HTTPException: Si el contacto no existe o hay un error
    """
    try:
        result = self.supabase.table('contacts').delete().eq('id', contact_id).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contacto no encontrado"
            )

        return True
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el contacto: {str(e)}"
        )
```

#### Listado y Búsqueda de Contactos

```python
async def list_contacts(self, skip: int = 0, limit: int = 100, list_id: Optional[str] = None) -> List[Contact]:
    """
    Lista contactos con paginación y filtros opcionales.

    Args:
        skip: Número de registros a omitir (paginación)
        limit: Número máximo de registros a devolver
        list_id: ID de lista de contactos para filtrar (opcional)

    Returns:
        List[Contact]: Lista de contactos

    Raises:
        Exception: Si hay un error al listar los contactos
    """
    if list_id:
        # Obtener contactos de una lista específica
        result = self.supabase.table('contact_list_contacts')\
            .select('contacts(*)')\
            .eq('list_id', list_id)\
            .range(skip, skip + limit - 1)\
            .execute()
        return [Contact(**contact['contacts']) for contact in result.data]
    else:
        # Obtener todos los contactos
        result = self.supabase.table('contacts')\
            .select('*')\
            .range(skip, skip + limit - 1)\
            .execute()
        return [Contact(**contact) for contact in result.data]

async def search_contacts(self, search_term: str, limit: int = 10) -> List[Contact]:
    """
    Busca contactos por nombre, email o número de teléfono.

    Args:
        search_term: Término de búsqueda
        limit: Número máximo de resultados

    Returns:
        List[Contact]: Lista de contactos que coinciden con la búsqueda

    Raises:
        HTTPException: Si hay un error en la búsqueda
    """
    try:
        # Buscar en nombre
        name_query = self.supabase.table('contacts').select('*').ilike('name', f'%{search_term}%').limit(limit)
        name_result = name_query.execute()

        # Si no hay suficientes resultados, buscar también en email y teléfono
        if not name_result.data or len(name_result.data) < limit:
            remaining = limit - (len(name_result.data) if name_result.data else 0)

            # Buscar en email
            email_query = self.supabase.table('contacts').select('*').ilike('email', f'%{search_term}%').limit(remaining)
            email_result = email_query.execute()

            # Buscar en teléfono
            phone_query = self.supabase.table('contacts').select('*').ilike('phone_number', f'%{search_term}%').limit(remaining)
            phone_result = phone_query.execute()

            # Combinar resultados
            all_results = []
            if name_result.data:
                all_results.extend(name_result.data)
            if email_result.data:
                all_results.extend(email_result.data)
            if phone_result.data:
                all_results.extend(phone_result.data)

            # Eliminar duplicados
            seen_ids = set()
            unique_results = []
            for item in all_results:
                if item['id'] not in seen_ids:
                    seen_ids.add(item['id'])
                    unique_results.append(item)

            return [Contact(**item) for item in unique_results[:limit]]

        return [Contact(**item) for item in name_result.data]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar contactos: {str(e)}"
        )
```

#### Gestión de Listas de Contactos

```python
async def create_contact_list(self, contact_list: ContactListCreate) -> ContactList:
    """
    Crea una nueva lista de contactos.

    Args:
        contact_list: Datos de la lista a crear

    Returns:
        ContactList: La lista creada

    Raises:
        HTTPException: Si hay un error al crear la lista
    """
    try:
        result = self.supabase.table('contact_lists').insert(contact_list.model_dump()).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear la lista de contactos"
            )

        return ContactList(**result.data[0])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la lista de contactos: {str(e)}"
        )

async def get_contact_list(self, list_id: str) -> ContactList:
    """
    Obtiene una lista de contactos por su ID.

    Args:
        list_id: ID de la lista

    Returns:
        ContactList: La lista encontrada

    Raises:
        HTTPException: Si la lista no existe o hay un error
    """
    try:
        result = self.supabase.table('contact_lists').select('*').eq('id', list_id).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lista de contactos no encontrada"
            )

        return ContactList(**result.data[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la lista de contactos: {str(e)}"
        )

async def add_contacts_to_list(self, list_id: str, contact_ids: List[str]) -> int:
    """
    Añade contactos a una lista.

    Args:
        list_id: ID de la lista
        contact_ids: Lista de IDs de contactos

    Returns:
        int: Número de contactos añadidos

    Raises:
        HTTPException: Si la lista no existe o hay un error
    """
    try:
        # Verificar que la lista existe
        await self.get_contact_list(list_id)

        # Preparar datos para inserción
        now = datetime.now().isoformat()
        data = [
            {
                "list_id": list_id,
                "contact_id": contact_id,
                "created_at": now
            }
            for contact_id in contact_ids
        ]

        # Insertar en tabla de relación
        result = self.supabase.table('contact_list_contacts').insert(data).execute()

        if not result.data:
            return 0

        return len(result.data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al añadir contactos a la lista: {str(e)}"
        )

async def remove_contact_from_list(self, list_id: str, contact_id: str) -> bool:
    """
    Elimina un contacto de una lista.

    Args:
        list_id: ID de la lista
        contact_id: ID del contacto

    Returns:
        bool: True si se eliminó correctamente

    Raises:
        HTTPException: Si la relación no existe o hay un error
    """
    try:
        result = self.supabase.table('contact_list_contacts').delete().eq('list_id', list_id).eq('contact_id', contact_id).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contacto no encontrado en la lista"
            )

        return True
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar contacto de la lista: {str(e)}"
        )
```

#### Importación y Exportación

```python
async def import_contacts_from_csv(self, file: UploadFile) -> Dict[str, int]:
    """
    Importa contactos desde un archivo CSV.

    Args:
        file: Archivo CSV a importar

    Returns:
        Dict[str, int]: Estadísticas de importación

    Raises:
        HTTPException: Si hay un error en la importación
    """
    try:
        # Leer contenido del archivo
        content = await file.read()

        # Decodificar y procesar CSV
        text = content.decode('utf-8')
        reader = csv.DictReader(io.StringIO(text))

        # Validar estructura del CSV
        required_fields = ['name', 'phone_number']
        csv_fields = reader.fieldnames

        if not all(field in csv_fields for field in required_fields):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El archivo CSV debe contener los campos: {', '.join(required_fields)}"
            )

        # Procesar filas
        success_count = 0
        error_count = 0

        for row in reader:
            try:
                # Validar datos
                if not row['name'] or not row['phone_number']:
                    error_count += 1
                    continue

                # Crear contacto
                contact_data = {
                    'name': row['name'],
                    'phone_number': row['phone_number'],
                    'email': row.get('email', None),
                    'notes': row.get('notes', None),
                    'tags': row.get('tags', '').split(',') if row.get('tags') else []
                }

                await self.create_contact(ContactCreate(**contact_data))
                success_count += 1
            except Exception:
                error_count += 1

        return {
            'total': success_count + error_count,
            'success': success_count,
            'errors': error_count
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al importar contactos: {str(e)}"
        )

async def export_contacts_to_csv(self, list_id: Optional[str] = None) -> str:
    """
    Exporta contactos a formato CSV.

    Args:
        list_id: ID de lista para filtrar (opcional)

    Returns:
        str: Contenido del CSV

    Raises:
        HTTPException: Si hay un error en la exportación
    """
    try:
        # Obtener contactos
        contacts = await self.list_contacts(limit=10000, list_id=list_id)

        if not contacts:
            return "name,phone_number,email,notes,tags\n"

        # Crear CSV en memoria
        output = io.StringIO()
        writer = csv.writer(output)

        # Escribir encabezados
        writer.writerow(['name', 'phone_number', 'email', 'notes', 'tags'])

        # Escribir datos
        for contact in contacts:
            writer.writerow([
                contact.name,
                contact.phone_number,
                contact.email or '',
                contact.notes or '',
                ','.join(contact.tags) if contact.tags else ''
            ])

        return output.getvalue()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al exportar contactos: {str(e)}"
        )
```

## Configuración

El servicio de contactos no requiere configuración específica más allá del cliente de Supabase que se inyecta en el constructor.

## Uso

### Inicialización

```python
# En app/main.py
from app.services.contact_service import ContactService
from app.config.supabase import supabase_client

contact_service = ContactService(supabase_client=supabase_client)
```

### Uso en Endpoints

```python
# En app/routers/contacts.py
@router.post("/", response_model=Contact)
async def create_contact(contact: ContactCreate):
    """Crea un nuevo contacto."""
    return await contact_service.create_contact(contact)

@router.get("/{contact_id}", response_model=Contact)
async def get_contact(contact_id: str):
    """Obtiene un contacto por su ID."""
    return await contact_service.get_contact(contact_id)

@router.put("/{contact_id}", response_model=Contact)
async def update_contact(contact_id: str, contact: ContactUpdate):
    """Actualiza un contacto existente."""
    return await contact_service.update_contact(contact_id, contact)

@router.delete("/{contact_id}", response_model=bool)
async def delete_contact(contact_id: str):
    """Elimina un contacto."""
    return await contact_service.delete_contact(contact_id)

@router.get("/", response_model=List[Contact])
async def list_contacts(skip: int = 0, limit: int = 100, list_id: Optional[str] = None):
    """Lista contactos con paginación y filtros opcionales."""
    return await contact_service.list_contacts(skip, limit, list_id)

@router.get("/search", response_model=List[Contact])
async def search_contacts(q: str, limit: int = 10):
    """Busca contactos por nombre, email o número de teléfono."""
    return await contact_service.search_contacts(q, limit)

# En app/routers/contact_lists.py
@router.post("/", response_model=ContactList)
async def create_contact_list(contact_list: ContactListCreate):
    """Crea una nueva lista de contactos."""
    return await contact_service.create_contact_list(contact_list)

@router.post("/{list_id}/contacts", response_model=int)
async def add_contacts_to_list(list_id: str, contact_ids: List[str]):
    """Añade contactos a una lista."""
    return await contact_service.add_contacts_to_list(list_id, contact_ids)

@router.post("/import", response_model=Dict[str, int])
async def import_contacts(file: UploadFile = File(...)):
    """Importa contactos desde un archivo CSV."""
    return await contact_service.import_contacts_from_csv(file)

@router.get("/export", response_class=PlainTextResponse)
async def export_contacts(list_id: Optional[str] = None):
    """Exporta contactos a formato CSV."""
    csv_content = await contact_service.export_contacts_to_csv(list_id)
    return PlainTextResponse(
        content=csv_content,
        headers={
            "Content-Disposition": "attachment; filename=contacts.csv"
        }
    )
```

## Flujo de Trabajo de Contactos

1. **Creación**: Se crean contactos individuales o se importan desde CSV
2. **Organización**: Se crean listas y se asignan contactos
3. **Asignación**: Se asignan listas a campañas
4. **Actualización**: Se mantiene la información de contactos actualizada
5. **Exportación**: Se exportan contactos para análisis o respaldo

## Consideraciones de Rendimiento

- **Paginación**: Implementación de paginación para grandes conjuntos de datos
- **Índices**: Uso de índices en la base de datos para consultas frecuentes
- **Procesamiento por lotes**: Importación y exportación en lotes para grandes volúmenes
- **Validación eficiente**: Optimización de la validación de datos durante la importación
- **Consultas optimizadas**: Minimizar el número de consultas a la base de datos

## Consideraciones de Seguridad

- **Validación de entrada**: Validación de todos los datos de entrada
- **Sanitización de datos**: Limpieza de datos antes de procesarlos
- **Protección de datos personales**: Cumplimiento con regulaciones de privacidad
- **Control de acceso**: Implementación de políticas de acceso basadas en roles
- **Auditoría**: Registro de operaciones sensibles

## Solución de Problemas

### Problemas Comunes

1. **Errores de importación**:
   - Verificar formato del archivo CSV
   - Comprobar campos requeridos
   - Revisar validación de números de teléfono

2. **Contactos duplicados**:
   - Implementar detección de duplicados
   - Verificar criterios de unicidad
   - Considerar estrategias de fusión

3. **Problemas de rendimiento**:
   - Monitorear tiempos de respuesta
   - Optimizar consultas para grandes volúmenes
   - Implementar caché para consultas frecuentes

4. **Errores de validación**:
   - Verificar formato de números de teléfono
   - Comprobar validación de email
   - Revisar logs para errores específicos

### Comandos Útiles

```bash
# Verificar logs
tail -f logs/contact_service.log

# Consultar contactos
curl http://localhost:8000/api/v1/contacts

# Buscar contactos
curl http://localhost:8000/api/v1/contacts/search?q=john
```

## Referencias

- [Supabase Documentation](https://supabase.io/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [CSV Module Documentation](https://docs.python.org/3/library/csv.html)
