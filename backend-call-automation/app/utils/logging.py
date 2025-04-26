"""
Módulo para configuración de logging estructurado.

Este módulo proporciona funciones para configurar y utilizar
un sistema de logging estructurado en formato JSON.
"""

import json
import logging
import sys
import time
import uuid
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, Optional, Union

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

# Configuración de niveles de log
LOG_LEVEL_MAP = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}

class JsonFormatter(logging.Formatter):
    """
    Formateador personalizado para logs en formato JSON.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Formatea un registro de log como JSON.

        Args:
            record: Registro de log a formatear

        Returns:
            Cadena JSON con el registro formateado
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "process": record.process
        }

        # Añadir contexto adicional si existe
        if hasattr(record, "context") and record.context:
            log_data.update(record.context)

        # Añadir excepción si existe
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info)
            }

        return json.dumps(log_data)

def setup_logging(
    app_name: str,
    level: str = "info",
    log_file: Optional[str] = None,
    console: bool = True
) -> logging.Logger:
    """
    Configura el sistema de logging.

    Args:
        app_name: Nombre de la aplicación
        level: Nivel de log (debug, info, warning, error, critical)
        log_file: Ruta al archivo de log (opcional)
        console: Si es True, también se loguea a la consola

    Returns:
        Logger configurado
    """
    # Crear logger
    logger = logging.getLogger(app_name)
    logger.setLevel(LOG_LEVEL_MAP.get(level.lower(), logging.INFO))

    # Limpiar handlers existentes
    logger.handlers = []

    # Crear formateador JSON
    formatter = JsonFormatter()

    # Añadir handler de archivo si se especifica
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Añadir handler de consola si se solicita
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para logging de solicitudes HTTP.
    """

    def __init__(
        self,
        app: ASGIApp,
        logger: logging.Logger,
        exclude_paths: Optional[list] = None
    ):
        """
        Inicializa el middleware.

        Args:
            app: Aplicación ASGI
            logger: Logger a utilizar
            exclude_paths: Lista de rutas a excluir del logging
        """
        super().__init__(app)
        self.logger = logger
        self.exclude_paths = exclude_paths or []

    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        """
        Procesa una solicitud HTTP y registra información de logging.

        Args:
            request: Solicitud HTTP
            call_next: Función para continuar el procesamiento

        Returns:
            Respuesta HTTP
        """
        # Generar ID de solicitud
        request_id = str(uuid.uuid4())

        # Verificar si la ruta debe ser excluida
        path = request.url.path
        if any(path.startswith(excluded) for excluded in self.exclude_paths):
            return await call_next(request)

        # Registrar inicio de solicitud
        start_time = time.time()

        # Añadir request_id a la solicitud para uso en controladores
        request.state.request_id = request_id

        # Procesar solicitud
        try:
            response = await call_next(request)

            # Calcular tiempo de procesamiento
            process_time = time.time() - start_time

            # Registrar solicitud completada
            self.logger.info(
                f"{request.method} {path} {response.status_code}",
                extra={
                    "context": {
                        "request_id": request_id,
                        "method": request.method,
                        "path": path,
                        "status_code": response.status_code,
                        "process_time_ms": round(process_time * 1000, 2),
                        "client_ip": request.client.host if request.client else None,
                        "user_agent": request.headers.get("user-agent")
                    }
                }
            )

            # Añadir request_id a la respuesta
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:
            # Registrar error
            self.logger.error(
                f"Error processing {request.method} {path}",
                extra={
                    "context": {
                        "request_id": request_id,
                        "method": request.method,
                        "path": path,
                        "client_ip": request.client.host if request.client else None,
                        "error": str(e)
                    }
                },
                exc_info=True
            )
            raise

def log_function_call(logger: logging.Logger):
    """
    Decorador para loguear llamadas a funciones.

    Args:
        logger: Logger a utilizar

    Returns:
        Decorador configurado
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generar ID de operación
            operation_id = str(uuid.uuid4())

            # Registrar inicio de operación
            start_time = time.time()
            logger.debug(
                f"Starting {func.__name__}",
                extra={
                    "context": {
                        "operation_id": operation_id,
                        "function": func.__name__,
                        "module": func.__module__,
                        "args": str(args),
                        "kwargs": str(kwargs)
                    }
                }
            )

            try:
                # Ejecutar función
                result = await func(*args, **kwargs)

                # Calcular tiempo de ejecución
                execution_time = time.time() - start_time

                # Registrar finalización exitosa
                logger.debug(
                    f"Completed {func.__name__}",
                    extra={
                        "context": {
                            "operation_id": operation_id,
                            "function": func.__name__,
                            "execution_time_ms": round(execution_time * 1000, 2),
                            "success": True
                        }
                    }
                )

                return result

            except Exception as e:
                # Calcular tiempo de ejecución
                execution_time = time.time() - start_time

                # Registrar error
                logger.error(
                    f"Error in {func.__name__}: {str(e)}",
                    extra={
                        "context": {
                            "operation_id": operation_id,
                            "function": func.__name__,
                            "execution_time_ms": round(execution_time * 1000, 2),
                            "success": False,
                            "error": str(e)
                        }
                    },
                    exc_info=True
                )
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generar ID de operación
            operation_id = str(uuid.uuid4())

            # Registrar inicio de operación
            start_time = time.time()
            logger.debug(
                f"Starting {func.__name__}",
                extra={
                    "context": {
                        "operation_id": operation_id,
                        "function": func.__name__,
                        "module": func.__module__,
                        "args": str(args),
                        "kwargs": str(kwargs)
                    }
                }
            )

            try:
                # Ejecutar función
                result = func(*args, **kwargs)

                # Calcular tiempo de ejecución
                execution_time = time.time() - start_time

                # Registrar finalización exitosa
                logger.debug(
                    f"Completed {func.__name__}",
                    extra={
                        "context": {
                            "operation_id": operation_id,
                            "function": func.__name__,
                            "execution_time_ms": round(execution_time * 1000, 2),
                            "success": True
                        }
                    }
                )

                return result

            except Exception as e:
                # Calcular tiempo de ejecución
                execution_time = time.time() - start_time

                # Registrar error
                logger.error(
                    f"Error in {func.__name__}: {str(e)}",
                    extra={
                        "context": {
                            "operation_id": operation_id,
                            "function": func.__name__,
                            "execution_time_ms": round(execution_time * 1000, 2),
                            "success": False,
                            "error": str(e)
                        }
                    },
                    exc_info=True
                )
                raise

        # Usar el wrapper adecuado según si la función es asíncrona o no
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator

def setup_app_logging(app: FastAPI, logger: logging.Logger, exclude_paths: Optional[list] = None) -> None:
    """
    Configura el logging para una aplicación FastAPI.

    Args:
        app: Aplicación FastAPI
        logger: Logger a utilizar
        exclude_paths: Lista de rutas a excluir del logging
    """
    # Añadir middleware de logging
    app.add_middleware(
        LoggingMiddleware,
        logger=logger,
        exclude_paths=exclude_paths or ["/health", "/metrics"]
    )

    # Añadir evento de inicio
    @app.on_event("startup")
    async def startup_event():
        logger.info(
            "Application startup",
            extra={
                "context": {
                    "event": "startup",
                    "app_name": app.title,
                    "app_version": app.version
                }
            }
        )

    # Añadir evento de cierre
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info(
            "Application shutdown",
            extra={
                "context": {
                    "event": "shutdown",
                    "app_name": app.title,
                    "app_version": app.version
                }
            }
        )

# Crear logger global
import asyncio
import os

# Asegurarse de que el directorio de logs existe
os.makedirs("logs", exist_ok=True)

app_logger = setup_logging(
    app_name="call-automation",
    level="info",
    log_file="logs/app.log",
    console=True
)
