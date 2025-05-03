"""
Servicio para la gestión de contactos.

Este módulo proporciona una interfaz para gestionar contactos y listas de contactos,
incluyendo operaciones CRUD, importación/exportación y asignación a campañas.

Classes:
    ContactService: Clase principal que gestiona las operaciones de contactos.

Dependencies:
    - Supabase: Para la persistencia de datos
    - FastAPI: Para el manejo de excepciones HTTP
    - CSV: Para importación y exportación de contactos
"""

import csv
import io

from fastapi import HTTPException, UploadFile, status

from app.models.contact import Contact, ContactCreate, ContactList, ContactListCreate, ContactUpdate


class ContactService:
    """
    Servicio para gestionar operaciones relacionadas con contactos.

    Este servicio proporciona métodos para crear, actualizar, eliminar y listar
    contactos, así como gestionar listas de contactos y sus asignaciones a campañas.

    Attributes:
        supabase: Cliente de Supabase para operaciones de base de datos

    Dependencies:
        - supabase_client: Cliente de Supabase para operaciones de base de datos
    """

    def __init__(self, supabase_client) -> None:
        """
        Inicializa el servicio de contactos.

        Args:
            supabase_client: Cliente de Supabase para operaciones de base de datos
        """
        self.supabase = supabase_client

    async def create_contact(self, contact_data: ContactCreate) -> Contact:
        """
        Crea un nuevo contacto en el sistema.

        Args:
            contact_data (ContactCreate): Datos del contacto a crear

        Returns:
            Contact: Objeto con la información del contacto creado

        Raises:
            HTTPException: Si hay un error al crear el contacto
        """
        try:
            result = self.supabase.table("contacts").insert(contact_data.model_dump()).execute()
            return Contact(**result.data[0])
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear el contacto: {e!s}",
            )

    async def get_contact(self, contact_id: str) -> Contact:
        """
        Obtiene la información de un contacto específico.

        Args:
            contact_id (str): ID del contacto a obtener

        Returns:
            Contact: Objeto con la información del contacto

        Raises:
            HTTPException: Si el contacto no existe
        """
        try:
            result = (
                self.supabase.table("contacts").select("*").eq("id", contact_id).single().execute()
            )
            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado"
                )
            return Contact(**result.data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener el contacto: {e!s}",
            )

    async def list_contacts(
        self,
        skip: int = 0,
        limit: int = 10,
        search: str | None = None,
        tags: list[str] | None = None,
    ) -> tuple[list[Contact], int]:
        """
        Lista los contactos con opciones de filtrado y paginación.

        Args:
            skip (int): Número de registros a saltar (paginación)
            limit (int): Número máximo de registros a devolver
            search (Optional[str]): Texto para buscar en nombre, email o teléfono
            tags (Optional[List[str]]): Lista de etiquetas para filtrar

        Returns:
            Tuple[List[Contact], int]: Lista de contactos y total de registros

        Raises:
            HTTPException: Si hay un error al listar los contactos
        """
        try:
            # Iniciar la consulta
            query = self.supabase.table("contacts").select("*", count="exact")

            # Aplicar filtros
            if search:
                query = query.or_(
                    f"name.ilike.%{search}%,email.ilike.%{search}%,phone_number.ilike.%{search}%"
                )

            if tags and len(tags) > 0:
                # Filtrar por tags (esto depende de cómo estén almacenados los tags)
                for tag in tags:
                    query = query.contains("tags", [tag])

            # Obtener el total de registros
            count_result = query.execute()
            total = count_result.count if hasattr(count_result, "count") else 0

            # Aplicar paginación
            result = query.range(skip, skip + limit - 1).execute()

            contacts = [Contact(**contact) for contact in result.data]
            return contacts, total
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al listar los contactos: {e!s}",
            )

    async def search_contacts(self, query: str, limit: int = 10) -> list[Contact]:
        """
        Busca contactos por nombre, email o número de teléfono.

        Args:
            query (str): Texto a buscar
            limit (int): Número máximo de resultados

        Returns:
            List[Contact]: Lista de contactos que coinciden con la búsqueda
        """
        try:
            result = (
                self.supabase.table("contacts")
                .select("*")
                .or_(f"name.ilike.%{query}%,email.ilike.%{query}%,phone_number.ilike.%{query}%")
                .limit(limit)
                .execute()
            )

            return [Contact(**contact) for contact in result.data]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al buscar contactos: {e!s}",
            )

    async def update_contact(self, contact_id: str, contact_data: ContactUpdate) -> Contact:
        """
        Actualiza la información de un contacto.

        Args:
            contact_id (str): ID del contacto a actualizar
            contact_data (ContactUpdate): Nuevos datos del contacto

        Returns:
            Contact: Objeto con la información actualizada del contacto

        Raises:
            HTTPException: Si el contacto no existe o hay un error en la actualización
        """
        try:
            # Filtrar campos None para no sobrescribir con valores nulos
            update_data = {k: v for k, v in contact_data.model_dump().items() if v is not None}

            result = (
                self.supabase.table("contacts").update(update_data).eq("id", contact_id).execute()
            )

            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado"
                )

            return Contact(**result.data[0])
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar el contacto: {e!s}",
            )

    async def delete_contact(self, contact_id: str) -> bool:
        """
        Elimina un contacto del sistema.

        Args:
            contact_id (str): ID del contacto a eliminar

        Returns:
            bool: True si se eliminó correctamente

        Raises:
            HTTPException: Si el contacto no existe o hay un error en la eliminación
        """
        try:
            result = self.supabase.table("contacts").delete().eq("id", contact_id).execute()

            if not result.data:
                return False

            return True
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar el contacto: {e!s}",
            )

    async def import_contacts_from_csv(self, file: UploadFile) -> dict[str, int]:
        """
        Importa contactos desde un archivo CSV.

        Args:
            file (UploadFile): Archivo CSV con los contactos a importar

        Returns:
            Dict[str, int]: Estadísticas de importación (contactos importados, errores)

        Raises:
            HTTPException: Si hay un error en la importación
        """
        try:
            # Leer el archivo CSV
            contents = await file.read()
            csv_file = io.StringIO(contents.decode("utf-8"))
            csv_reader = csv.DictReader(csv_file)

            # Estadísticas de importación
            stats = {"total": 0, "imported": 0, "errors": 0}

            # Procesar cada fila
            contacts_to_import = []

            for row in csv_reader:
                stats["total"] += 1

                try:
                    # Validar datos mínimos
                    if not row.get("name") or not row.get("phone_number"):
                        stats["errors"] += 1
                        continue

                    # Crear objeto de contacto
                    contact_data = {
                        "name": row.get("name"),
                        "phone_number": row.get("phone_number"),
                        "email": row.get("email", None),
                        "notes": row.get("notes", None),
                        "tags": row.get("tags", "").split(",") if row.get("tags") else [],
                    }

                    # Validar con Pydantic
                    contact = ContactCreate(**contact_data)
                    contacts_to_import.append(contact.model_dump())

                except Exception:
                    stats["errors"] += 1

            # Importar contactos en lotes de 100
            batch_size = 100
            for i in range(0, len(contacts_to_import), batch_size):
                batch = contacts_to_import[i : i + batch_size]
                result = self.supabase.table("contacts").insert(batch).execute()
                stats["imported"] += len(result.data)

            return stats

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al importar contactos: {e!s}",
            )

    async def export_contacts_to_csv(self, list_id: str | None = None) -> str:
        """
        Exporta contactos a formato CSV.

        Args:
            list_id (Optional[str]): ID de la lista de contactos (opcional)

        Returns:
            str: Contenido del archivo CSV

        Raises:
            HTTPException: Si hay un error en la exportación
        """
        try:
            # Obtener contactos
            if list_id:
                # Obtener contactos de una lista específica
                result = (
                    self.supabase.table("contact_list_contacts")
                    .select("contacts(*)")
                    .eq("list_id", list_id)
                    .execute()
                )
                contacts = [contact["contacts"] for contact in result.data]
            else:
                # Obtener todos los contactos
                result = self.supabase.table("contacts").select("*").execute()
                contacts = result.data

            # Crear archivo CSV en memoria
            output = io.StringIO()
            fieldnames = [
                "id",
                "name",
                "phone_number",
                "email",
                "notes",
                "tags",
                "created_at",
                "updated_at",
            ]
            writer = csv.DictWriter(output, fieldnames=fieldnames)

            # Escribir encabezado
            writer.writeheader()

            # Escribir filas
            for contact in contacts:
                # Convertir tags a string si es una lista
                if "tags" in contact and isinstance(contact["tags"], list):
                    contact["tags"] = ",".join(contact["tags"])
                writer.writerow(contact)

            return output.getvalue()

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al exportar contactos: {e!s}",
            )

    async def list_contact_lists(self) -> list[ContactList]:
        """
        Lista todas las listas de contactos.

        Returns:
            List[ContactList]: Lista de listas de contactos
        """
        try:
            result = self.supabase.table("contact_lists").select("*").execute()
            return [ContactList(**contact_list) for contact_list in result.data]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al listar las listas de contactos: {e!s}",
            )

    async def get_contact_list(self, list_id: str) -> ContactList:
        """
        Obtiene una lista de contactos por su ID.

        Args:
            list_id (str): ID de la lista de contactos

        Returns:
            ContactList: Datos de la lista de contactos

        Raises:
            HTTPException: Si la lista no existe
        """
        try:
            result = (
                self.supabase.table("contact_lists")
                .select("*")
                .eq("id", list_id)
                .single()
                .execute()
            )

            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Lista de contactos no encontrada"
                )

            return ContactList(**result.data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener la lista de contactos: {e!s}",
            )

    async def create_contact_list(self, list_data: ContactListCreate) -> ContactList:
        """
        Crea una nueva lista de contactos.

        Args:
            list_data (ContactListCreate): Datos de la lista a crear

        Returns:
            ContactList: Objeto con la información de la lista creada

        Raises:
            HTTPException: Si hay un error al crear la lista
        """
        try:
            result = self.supabase.table("contact_lists").insert(list_data.model_dump()).execute()
            return ContactList(**result.data[0])
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear la lista de contactos: {e!s}",
            )

    async def add_contacts_to_list(self, list_id: str, contact_ids: list[str]) -> int:
        """
        Agrega contactos a una lista existente.

        Args:
            list_id (str): ID de la lista de contactos
            contact_ids (List[str]): Lista de IDs de contactos a agregar

        Returns:
            int: Número de contactos añadidos

        Raises:
            HTTPException: Si la lista no existe o hay un error en la operación
        """
        try:
            # Verificar que la lista existe
            list_result = (
                self.supabase.table("contact_lists")
                .select("*")
                .eq("id", list_id)
                .single()
                .execute()
            )
            if not list_result.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Lista de contactos no encontrada"
                )

            # Crear las relaciones
            relations = [
                {"list_id": list_id, "contact_id": contact_id} for contact_id in contact_ids
            ]

            result = self.supabase.table("contact_list_contacts").insert(relations).execute()
            return len(result.data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al añadir contactos a la lista: {e!s}",
            )

    async def remove_contact_from_list(self, list_id: str, contact_id: str) -> bool:
        """
        Elimina un contacto de una lista.

        Args:
            list_id (str): ID de la lista de contactos
            contact_id (str): ID del contacto a eliminar

        Returns:
            bool: True si se eliminó correctamente

        Raises:
            HTTPException: Si la lista o el contacto no existen
        """
        try:
            result = (
                self.supabase.table("contact_list_contacts")
                .delete()
                .eq("list_id", list_id)
                .eq("contact_id", contact_id)
                .execute()
            )

            return len(result.data) > 0
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar el contacto de la lista: {e!s}",
            )
