"""
Paquete de middleware para la aplicación.

Este paquete contiene los middleware utilizados en la aplicación.
"""

from app.middleware.error_handler import setup_error_handling
from app.middleware.auth_middleware import setup_auth_middleware

__all__ = ["setup_error_handling", "setup_auth_middleware"]
