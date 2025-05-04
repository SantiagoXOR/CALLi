"""
Paquete de middleware para la aplicación.

Este paquete contiene los middleware utilizados en la aplicación.
"""

from app.middleware.auth_middleware import setup_auth_middleware
from app.middleware.error_handler import setup_error_handling

__all__ = ["setup_auth_middleware", "setup_error_handling"]
