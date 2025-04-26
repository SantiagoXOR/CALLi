"""
Router para la autenticación con Supabase.

Este módulo define los endpoints para la autenticación
y gestión de usuarios con Supabase.
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.services.auth_service import AuthService
from app.config.dependencies import get_supabase_client
from app.utils.logging import app_logger as logger
from supabase import Client as SupabaseClient
from pydantic import BaseModel, EmailStr, Field

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Modelos de datos
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str
    phone: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    roles: List[str] = []

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: str
    user: UserResponse

@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    supabase_client: SupabaseClient = Depends(get_supabase_client)
) -> TokenResponse:
    """
    Inicia sesión con email y contraseña.
    
    Args:
        credentials: Credenciales de usuario
        
    Returns:
        TokenResponse con token de acceso y datos del usuario
    """
    try:
        # Iniciar sesión
        response = supabase_client.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        
        # Obtener datos de la sesión
        session = response.session
        user = response.user
        
        # Crear servicio de autenticación
        auth_service = AuthService(supabase_client)
        
        # Obtener roles del usuario
        roles = await auth_service.get_user_roles(user.id)
        
        # Crear respuesta
        return TokenResponse(
            access_token=session.access_token,
            expires_in=session.expires_in,
            refresh_token=session.refresh_token,
            user=UserResponse(
                id=user.id,
                email=user.email,
                name=user.user_metadata.get("name") if user.user_metadata else None,
                roles=roles
            )
        )
    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    supabase_client: SupabaseClient = Depends(get_supabase_client)
) -> UserResponse:
    """
    Registra un nuevo usuario.
    
    Args:
        user_data: Datos del usuario a registrar
        
    Returns:
        UserResponse con datos del usuario registrado
    """
    try:
        # Crear servicio de autenticación
        auth_service = AuthService(supabase_client)
        
        # Crear usuario
        user = await auth_service.create_user(
            email=user_data.email,
            password=user_data.password,
            user_metadata={
                "name": user_data.name,
                "phone": user_data.phone
            }
        )
        
        # Asignar rol por defecto
        await auth_service.assign_role(user["id"], "user")
        
        # Obtener roles del usuario
        roles = await auth_service.get_user_roles(user["id"])
        
        # Crear respuesta
        return UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["user_metadata"].get("name") if user["user_metadata"] else None,
            roles=roles
        )
    except Exception as e:
        logger.error(f"Error en registro: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar usuario: {str(e)}"
        )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str = Body(..., embed=True),
    supabase_client: SupabaseClient = Depends(get_supabase_client)
) -> TokenResponse:
    """
    Refresca un token de acceso.
    
    Args:
        refresh_token: Token de refresco
        
    Returns:
        TokenResponse con nuevo token de acceso
    """
    try:
        # Refrescar token
        response = supabase_client.auth.refresh_session(refresh_token)
        
        # Obtener datos de la sesión
        session = response.session
        user = response.user
        
        # Crear servicio de autenticación
        auth_service = AuthService(supabase_client)
        
        # Obtener roles del usuario
        roles = await auth_service.get_user_roles(user.id)
        
        # Crear respuesta
        return TokenResponse(
            access_token=session.access_token,
            expires_in=session.expires_in,
            refresh_token=session.refresh_token,
            user=UserResponse(
                id=user.id,
                email=user.email,
                name=user.user_metadata.get("name") if user.user_metadata else None,
                roles=roles
            )
        )
    except Exception as e:
        logger.error(f"Error al refrescar token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de refresco inválido"
        )

@router.post("/logout")
async def logout(
    supabase_client: SupabaseClient = Depends(get_supabase_client)
) -> Dict[str, bool]:
    """
    Cierra la sesión actual.
    
    Returns:
        Dict con confirmación de cierre de sesión
    """
    try:
        # Cerrar sesión
        supabase_client.auth.sign_out()
        
        return {"success": True}
    except Exception as e:
        logger.error(f"Error al cerrar sesión: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cerrar sesión: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    supabase_client: SupabaseClient = Depends(get_supabase_client)
) -> UserResponse:
    """
    Obtiene información del usuario actual.
    
    Returns:
        UserResponse con datos del usuario actual
    """
    try:
        # Obtener usuario actual
        response = supabase_client.auth.get_user()
        user = response.user
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No autenticado"
            )
        
        # Crear servicio de autenticación
        auth_service = AuthService(supabase_client)
        
        # Obtener roles del usuario
        roles = await auth_service.get_user_roles(user.id)
        
        # Crear respuesta
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.user_metadata.get("name") if user.user_metadata else None,
            roles=roles
        )
    except Exception as e:
        logger.error(f"Error al obtener usuario actual: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado"
        )
