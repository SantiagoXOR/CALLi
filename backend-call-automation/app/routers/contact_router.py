"""
Router para la gestión de contactos.

Este módulo define los endpoints para la gestión de contactos, incluyendo
operaciones CRUD, importación y exportación de contactos.
"""

# Importaciones de biblioteca estándar

# Importaciones de terceros

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import PlainTextResponse

# Importaciones del proyecto
from app.dependencies import get_supabase_client
from app.models.contact import Contact, ContactCreate, ContactList, ContactListCreate, ContactUpdate
from app.services.contact_service import ContactService
from supabase import Client as SupabaseClient

router = APIRouter(prefix="/api/contacts", tags=["contacts"])


# Endpoints para contactos individuales
@router.get("/", response_model=dict[str, object])
async def list_contacts(
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
    tags: list[str] | None = None,
    supabase_client: SupabaseClient = Depends(get_supabase_client),
):
    """
    Lista los contactos con paginación y filtros opcionales.

    Args:
        skip: Número de registros a omitir (para paginación)
        limit: Número máximo de registros a devolver
        search: Texto para buscar en nombre, email o teléfono
        tags: Lista de etiquetas para filtrar

    Returns:
        Dict con datos de contactos y metadatos de paginación
    """
    contact_service = ContactService(supabase_client)
    contacts, total = await contact_service.list_contacts(skip, limit, search, tags)

    return {
        "data": contacts,
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "limit": limit,
        "totalPages": (total + limit - 1) // limit if limit > 0 else 1,
    }


@router.get("/search", response_model=list[Contact])
async def search_contacts(
    q: str, limit: int = 10, supabase_client: SupabaseClient = Depends(get_supabase_client)
):
    """
    Busca contactos por nombre, email o número de teléfono.

    Args:
        q: Texto a buscar
        limit: Número máximo de resultados

    Returns:
        Lista de contactos que coinciden con la búsqueda
    """
    contact_service = ContactService(supabase_client)
    return await contact_service.search_contacts(q, limit)


@router.get("/{contact_id}", response_model=Contact)
async def get_contact(
    contact_id: str, supabase_client: SupabaseClient = Depends(get_supabase_client)
):
    """
    Obtiene un contacto por su ID.

    Args:
        contact_id: ID del contacto

    Returns:
        Datos del contacto

    Raises:
        HTTPException: Si el contacto no existe
    """
    contact_service = ContactService(supabase_client)
    contact = await contact_service.get_contact(contact_id)

    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")

    return contact


@router.post("/", response_model=Contact, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact: ContactCreate, supabase_client: SupabaseClient = Depends(get_supabase_client)
):
    """
    Crea un nuevo contacto.

    Args:
        contact: Datos del contacto a crear

    Returns:
        Contacto creado
    """
    contact_service = ContactService(supabase_client)
    return await contact_service.create_contact(contact)


@router.put("/{contact_id}", response_model=Contact)
async def update_contact(
    contact_id: str,
    contact: ContactUpdate,
    supabase_client: SupabaseClient = Depends(get_supabase_client),
):
    """
    Actualiza un contacto existente.

    Args:
        contact_id: ID del contacto a actualizar
        contact: Datos actualizados del contacto

    Returns:
        Contacto actualizado

    Raises:
        HTTPException: Si el contacto no existe
    """
    contact_service = ContactService(supabase_client)
    updated_contact = await contact_service.update_contact(contact_id, contact)

    if not updated_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")

    return updated_contact


@router.delete("/{contact_id}", response_model=dict[str, bool])
async def delete_contact(
    contact_id: str, supabase_client: SupabaseClient = Depends(get_supabase_client)
):
    """
    Elimina un contacto.

    Args:
        contact_id: ID del contacto a eliminar

    Returns:
        Confirmación de eliminación

    Raises:
        HTTPException: Si el contacto no existe o no se puede eliminar
    """
    contact_service = ContactService(supabase_client)
    success = await contact_service.delete_contact(contact_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contacto no encontrado o no se pudo eliminar",
        )

    return {"success": True}


# Endpoints para importación y exportación
@router.post("/import", response_model=dict[str, int])
async def import_contacts(
    file: UploadFile = File(...), supabase_client: SupabaseClient = Depends(get_supabase_client)
):
    """
    Importa contactos desde un archivo CSV.

    Args:
        file: Archivo CSV con los contactos a importar

    Returns:
        Estadísticas de importación (contactos importados, errores)
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El archivo debe ser CSV"
        )

    contact_service = ContactService(supabase_client)
    result = await contact_service.import_contacts_from_csv(file)
    return result


@router.get("/export", response_class=PlainTextResponse)
async def export_contacts(
    list_id: str | None = None, supabase_client: SupabaseClient = Depends(get_supabase_client)
):
    """
    Exporta contactos a formato CSV.

    Args:
        list_id: ID de la lista de contactos (opcional)

    Returns:
        Archivo CSV con los contactos
    """
    contact_service = ContactService(supabase_client)
    csv_content = await contact_service.export_contacts_to_csv(list_id)

    return PlainTextResponse(
        content=csv_content, headers={"Content-Disposition": "attachment; filename=contacts.csv"}
    )


# Endpoints para listas de contactos
@router.get("/lists", response_model=list[ContactList])
async def list_contact_lists(supabase_client: SupabaseClient = Depends(get_supabase_client)):
    """
    Lista todas las listas de contactos.

    Returns:
        Lista de listas de contactos
    """
    contact_service = ContactService(supabase_client)
    return await contact_service.list_contact_lists()


@router.get("/lists/{list_id}", response_model=ContactList)
async def get_contact_list(
    list_id: str, supabase_client: SupabaseClient = Depends(get_supabase_client)
):
    """
    Obtiene una lista de contactos por su ID.

    Args:
        list_id: ID de la lista de contactos

    Returns:
        Datos de la lista de contactos

    Raises:
        HTTPException: Si la lista no existe
    """
    contact_service = ContactService(supabase_client)
    contact_list = await contact_service.get_contact_list(list_id)

    if not contact_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lista de contactos no encontrada"
        )

    return contact_list


@router.post("/lists", response_model=ContactList, status_code=status.HTTP_201_CREATED)
async def create_contact_list(
    contact_list: ContactListCreate, supabase_client: SupabaseClient = Depends(get_supabase_client)
):
    """
    Crea una nueva lista de contactos.

    Args:
        contact_list: Datos de la lista de contactos a crear

    Returns:
        Lista de contactos creada
    """
    contact_service = ContactService(supabase_client)
    return await contact_service.create_contact_list(contact_list)


@router.post("/lists/{list_id}/contacts", response_model=dict[str, int])
async def add_contacts_to_list(
    list_id: str,
    contact_ids: list[str],
    supabase_client: SupabaseClient = Depends(get_supabase_client),
):
    """
    Añade contactos a una lista.

    Args:
        list_id: ID de la lista de contactos
        contact_ids: Lista de IDs de contactos a añadir

    Returns:
        Número de contactos añadidos

    Raises:
        HTTPException: Si la lista no existe
    """
    contact_service = ContactService(supabase_client)
    count = await contact_service.add_contacts_to_list(list_id, contact_ids)

    return {"added": count}


@router.delete("/lists/{list_id}/contacts/{contact_id}", response_model=dict[str, bool])
async def remove_contact_from_list(
    list_id: str, contact_id: str, supabase_client: SupabaseClient = Depends(get_supabase_client)
):
    """
    Elimina un contacto de una lista.

    Args:
        list_id: ID de la lista de contactos
        contact_id: ID del contacto a eliminar

    Returns:
        Confirmación de eliminación

    Raises:
        HTTPException: Si la lista o el contacto no existen
    """
    contact_service = ContactService(supabase_client)
    success = await contact_service.remove_contact_from_list(list_id, contact_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lista o contacto no encontrados"
        )

    return {"success": True}
