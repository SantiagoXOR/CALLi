"""
Middleware para autenticación con Supabase.

Este módulo proporciona un middleware para verificar y validar
tokens JWT de Supabase en las solicitudes HTTP.
"""

import time
from collections.abc import Awaitable, Callable

import jwt  # PyJWT en lugar de python-jose
from fastapi import Request, status
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.config.settings import get_settings
from app.utils.logging import app_logger as logger

settings = get_settings()


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware para autenticación con Supabase.

    Este middleware verifica y valida tokens JWT de Supabase
    en las solicitudes HTTP.
    """

    def __init__(
        self,
        app: ASGIApp,
        public_routes: list[str] | None = None,
        public_route_prefixes: list[str] | None = None,
        jwt_secret: str | None = None,
        jwt_algorithms: list[str] | None = None,
    ) -> None:
        """
        Inicializa el middleware de autenticación.

        Args:
            app: Aplicación ASGI
            public_routes: Lista de rutas públicas (no requieren autenticación)
            public_route_prefixes: Lista de prefijos de rutas públicas
            jwt_secret: Secreto para verificar tokens JWT
            jwt_algorithms: Algoritmos permitidos para tokens JWT
        """
        super().__init__(app)
        self.public_routes = public_routes or []
        self.public_route_prefixes = public_route_prefixes or []
        self.jwt_secret = jwt_secret or settings.SUPABASE_JWT_SECRET
        self.jwt_algorithms = jwt_algorithms or ["HS256"]

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable]
    ) -> Response:
        """
        Procesa una solicitud HTTP y verifica la autenticación.

        Args:
            request: Solicitud HTTP
            call_next: Función para continuar el procesamiento

        Returns:
            Respuesta HTTP
        """
        # Verificar si la ruta es pública
        path = request.url.path

        # Rutas públicas exactas
        if path in self.public_routes:
            return await call_next(request)

        # Prefijos de rutas públicas
        for prefix in self.public_route_prefixes:
            if path.startswith(prefix):
                return await call_next(request)

        # Verificar token de autenticación
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "No se proporcionó token de autenticación"},
            )

        try:
            # Extraer token
            token_type, token = auth_header.split()
            if token_type.lower() != "bearer":
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Tipo de token no válido"},
                )

            # Verificar token
            payload = self._verify_token(token)

            # Añadir información de usuario a la solicitud
            request.state.user = payload
            request.state.user_id = payload.get("sub")
            request.state.user_roles = payload.get("role", "").split(",")

            # Continuar con la solicitud
            return await call_next(request)

        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Token expirado"}
            )
        except jwt.InvalidTokenError:
            # No exponer detalles específicos del error para evitar fugas de información
            logger.warning("Token inválido recibido en la solicitud")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token inválido"},
            )
        except Exception as e:
            logger.error(f"Error en middleware de autenticación: {e!s}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Error interno de autenticación"},
            )

    def _verify_token(self, token: str) -> dict:
        """
        Verifica un token JWT.

        Args:
            token: Token JWT a verificar

        Returns:
            Dict con la información del token

        Raises:
            jwt.InvalidTokenError: Si el token es inválido
        """
        # Verificar token
        payload = jwt.decode(
            token,
            self.jwt_secret,
            algorithms=self.jwt_algorithms,
            options={"verify_signature": True},
        )

        # Verificar expiración
        exp = payload.get("exp")
        if exp and exp < time.time():
            raise jwt.ExpiredSignatureError("Token expirado")

        return payload


def setup_auth_middleware(
    app: ASGIApp,
    public_routes: list[str] | None = None,
    public_route_prefixes: list[str] | None = None,
) -> None:
    """
    Configura el middleware de autenticación para una aplicación.

    Args:
        app: Aplicación ASGI
        public_routes: Lista de rutas públicas (no requieren autenticación)
        public_route_prefixes: Lista de prefijos de rutas públicas
    """
    # Rutas públicas por defecto
    default_public_routes = [
        "/",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/health",
        "/metrics",
    ]

    # Prefijos de rutas públicas por defecto
    default_public_prefixes = [
        "/api/auth",
        "/api/v1/auth",
        "/api/webhook",
    ]

    # Combinar con rutas proporcionadas
    all_public_routes = (public_routes or []) + default_public_routes
    all_public_prefixes = (public_route_prefixes or []) + default_public_prefixes

    # Añadir middleware
    app.add_middleware(
        AuthMiddleware, public_routes=all_public_routes, public_route_prefixes=all_public_prefixes
    )
