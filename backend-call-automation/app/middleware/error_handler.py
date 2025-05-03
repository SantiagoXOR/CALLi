"""
Middleware para manejo consistente de errores.

Este módulo proporciona un middleware para capturar y manejar
excepciones de forma consistente en toda la aplicación.
"""

import logging
import traceback

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# from typing import Any  # No se utiliza


class ErrorHandlerMiddleware:
    """
    Middleware para manejo consistente de errores.
    """

    def __init__(self, app: FastAPI, logger: logging.Logger) -> None:
        """
        Inicializa el middleware.

        Args:
            app: Aplicación FastAPI
            logger: Logger para registrar errores
        """
        self.app = app
        self.logger = logger

        # Registrar manejadores de excepciones
        app.add_exception_handler(StarletteHTTPException, self.http_exception_handler)
        app.add_exception_handler(RequestValidationError, self.validation_exception_handler)
        app.add_exception_handler(ValidationError, self.validation_exception_handler)
        app.add_exception_handler(Exception, self.generic_exception_handler)

    async def http_exception_handler(
        self, request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        """
        Maneja excepciones HTTP.

        Args:
            request: Solicitud HTTP
            exc: Excepción HTTP

        Returns:
            Respuesta JSON con información del error
        """
        # Obtener request_id si existe
        request_id = getattr(request.state, "request_id", None)

        # Construir respuesta
        error_response = {"status": "error", "code": exc.status_code, "message": str(exc.detail)}

        # Añadir request_id si existe
        if request_id:
            error_response["request_id"] = request_id

        # Loguear error si es 5xx
        if exc.status_code >= 500:
            self.logger.error(
                f"HTTP error {exc.status_code}: {exc.detail}",
                extra={
                    "context": {
                        "request_id": request_id,
                        "status_code": exc.status_code,
                        "path": request.url.path,
                        "method": request.method,
                    }
                },
            )

        return JSONResponse(status_code=exc.status_code, content=error_response)

    async def validation_exception_handler(
        self, request: Request, exc: RequestValidationError | ValidationError
    ) -> JSONResponse:
        """
        Maneja errores de validación.

        Args:
            request: Solicitud HTTP
            exc: Error de validación

        Returns:
            Respuesta JSON con información del error
        """
        # Obtener request_id si existe
        request_id = getattr(request.state, "request_id", None)

        # Extraer errores de validación
        errors = []
        for error in exc.errors():
            error_info = {
                "loc": error.get("loc", []),
                "msg": error.get("msg", ""),
                "type": error.get("type", ""),
            }
            errors.append(error_info)

        # Construir respuesta
        error_response = {
            "status": "error",
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "Error de validación",
            "errors": errors,
        }

        # Añadir request_id si existe
        if request_id:
            error_response["request_id"] = request_id

        # Loguear error
        self.logger.warning(
            "Validation error",
            extra={
                "context": {
                    "request_id": request_id,
                    "path": request.url.path,
                    "method": request.method,
                    "errors": errors,
                }
            },
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=error_response
        )

    async def generic_exception_handler(self, request: Request, exc: Exception) -> JSONResponse:
        """
        Maneja excepciones genéricas.

        Args:
            request: Solicitud HTTP
            exc: Excepción

        Returns:
            Respuesta JSON con información del error
        """
        # Obtener request_id si existe
        request_id = getattr(request.state, "request_id", None)

        # Construir respuesta
        error_response = {
            "status": "error",
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Error interno del servidor",
        }

        # Añadir request_id si existe
        if request_id:
            error_response["request_id"] = request_id

        # Loguear error
        self.logger.error(
            f"Unhandled exception: {exc!s}",
            extra={
                "context": {
                    "request_id": request_id,
                    "path": request.url.path,
                    "method": request.method,
                    "exception": str(exc),
                    "traceback": traceback.format_exc(),
                }
            },
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_response
        )


def setup_error_handling(app: FastAPI, logger: logging.Logger) -> None:
    """
    Configura el manejo de errores para una aplicación FastAPI.

    Args:
        app: Aplicación FastAPI
        logger: Logger para registrar errores
    """
    ErrorHandlerMiddleware(app, logger)
