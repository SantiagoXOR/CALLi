"""
Servicio para la autenticación con Supabase.

Este módulo proporciona funcionalidades para la autenticación
y gestión de usuarios con Supabase.
"""

from typing import Any

from fastapi import HTTPException, status

from app.config.settings import get_settings
from app.utils.logging import app_logger as logger
from supabase import Client as SupabaseClient

settings = get_settings()


class AuthService:
    """
    Servicio para la autenticación con Supabase.

    Este servicio proporciona métodos para la autenticación
    y gestión de usuarios con Supabase.
    """

    def __init__(self, supabase_client: SupabaseClient) -> None:
        """
        Inicializa el servicio de autenticación.

        Args:
            supabase_client: Cliente de Supabase
        """
        self.supabase = supabase_client

    async def get_user(self, user_id: str) -> dict[str, Any]:
        """
        Obtiene información de un usuario por su ID.

        Args:
            user_id: ID del usuario

        Returns:
            Dict con la información del usuario

        Raises:
            HTTPException: Si el usuario no existe
        """
        try:
            response = self.supabase.auth.admin.get_user_by_id(user_id)
            user = response.user

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
                )

            return {
                "id": user.id,
                "email": user.email,
                "phone": user.phone,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "last_sign_in_at": user.last_sign_in_at,
                "app_metadata": user.app_metadata,
                "user_metadata": user.user_metadata,
                "identities": user.identities,
            }
        except Exception as e:
            logger.error(f"Error al obtener usuario: {e!s}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener usuario: {e!s}",
            )

    async def get_user_by_email(self, email: str) -> dict[str, Any]:
        """
        Obtiene información de un usuario por su email.

        Args:
            email: Email del usuario

        Returns:
            Dict con la información del usuario

        Raises:
            HTTPException: Si el usuario no existe
        """
        try:
            # Buscar usuario por email
            response = self.supabase.auth.admin.list_users()
            users = response.users

            # Filtrar por email
            user = next((u for u in users if u.email == email), None)

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
                )

            return {
                "id": user.id,
                "email": user.email,
                "phone": user.phone,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "last_sign_in_at": user.last_sign_in_at,
                "app_metadata": user.app_metadata,
                "user_metadata": user.user_metadata,
                "identities": user.identities,
            }
        except Exception as e:
            logger.error(f"Error al obtener usuario por email: {e!s}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener usuario por email: {e!s}",
            )

    async def get_user_roles(self, user_id: str) -> list[str]:
        """
        Obtiene los roles de un usuario.

        Args:
            user_id: ID del usuario

        Returns:
            Lista de roles del usuario
        """
        try:
            # Obtener roles del usuario
            response = (
                self.supabase.table("user_roles").select("role").eq("user_id", user_id).execute()
            )

            # Extraer roles
            roles = [item["role"] for item in response.data]

            return roles
        except Exception as e:
            logger.error(f"Error al obtener roles de usuario: {e!s}")
            return []

    async def check_permission(self, user_id: str, permission: str) -> bool:
        """
        Verifica si un usuario tiene un permiso específico.

        Args:
            user_id: ID del usuario
            permission: Permiso a verificar

        Returns:
            True si el usuario tiene el permiso, False en caso contrario
        """
        try:
            # Obtener roles del usuario
            roles = await self.get_user_roles(user_id)

            # Verificar si algún rol tiene el permiso
            for role in roles:
                # Obtener permisos del rol
                response = (
                    self.supabase.table("role_permissions")
                    .select("permission")
                    .eq("role", role)
                    .execute()
                )

                # Extraer permisos
                permissions = [item["permission"] for item in response.data]

                # Verificar si el permiso está en la lista
                if permission in permissions:
                    return True

            return False
        except Exception as e:
            logger.error(f"Error al verificar permiso: {e!s}")
            return False

    async def create_user(
        self, email: str, password: str, user_metadata: dict[str, Any] = None
    ) -> dict[str, Any]:
        """
        Crea un nuevo usuario.

        Args:
            email: Email del usuario
            password: Contraseña del usuario
            user_metadata: Metadatos del usuario

        Returns:
            Dict con la información del usuario creado

        Raises:
            HTTPException: Si hay un error al crear el usuario
        """
        try:
            # Crear usuario
            response = self.supabase.auth.admin.create_user(
                {
                    "email": email,
                    "password": password,
                    "email_confirm": True,
                    "user_metadata": user_metadata or {},
                }
            )

            user = response.user

            return {
                "id": user.id,
                "email": user.email,
                "created_at": user.created_at,
                "user_metadata": user.user_metadata,
            }
        except Exception as e:
            logger.error(f"Error al crear usuario: {e!s}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear usuario: {e!s}",
            )

    async def assign_role(self, user_id: str, role: str) -> bool:
        """
        Asigna un rol a un usuario.

        Args:
            user_id: ID del usuario
            role: Rol a asignar

        Returns:
            True si se asignó correctamente, False en caso contrario
        """
        try:
            # Verificar si ya tiene el rol
            response = (
                self.supabase.table("user_roles")
                .select("*")
                .eq("user_id", user_id)
                .eq("role", role)
                .execute()
            )

            if response.data:
                # Ya tiene el rol
                return True

            # Asignar rol
            self.supabase.table("user_roles").insert({"user_id": user_id, "role": role}).execute()

            return True
        except Exception as e:
            logger.error(f"Error al asignar rol: {e!s}")
            return False

    async def remove_role(self, user_id: str, role: str) -> bool:
        """
        Elimina un rol de un usuario.

        Args:
            user_id: ID del usuario
            role: Rol a eliminar

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            # Eliminar rol
            self.supabase.table("user_roles").delete().eq("user_id", user_id).eq(
                "role", role
            ).execute()

            return True
        except Exception as e:
            logger.error(f"Error al eliminar rol: {e!s}")
            return False
