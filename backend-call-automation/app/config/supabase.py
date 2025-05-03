"""
Módulo de configuración del cliente Supabase.

Este módulo configura y exporta una instancia única del cliente Supabase
para ser utilizada en toda la aplicación. Utiliza variables de entorno
para la configuración de credenciales.

Variables de entorno requeridas:
    - SUPABASE_URL: URL de la instancia de Supabase
    - SUPABASE_KEY: Clave de acceso anónimo de Supabase
"""

import logging
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

from dotenv import load_dotenv

from supabase import Client, create_client

# Configurar logger
logger = logging.getLogger(__name__)


# Cargar variables de entorno según el entorno
def load_env_files():
    """Carga los archivos de variables de entorno apropiados."""
    # Directorio base del proyecto
    base_dir = Path(__file__).resolve().parent.parent.parent

    # Determinar qué archivo .env cargar
    if "pytest" in sys.modules:
        # Si estamos en un entorno de prueba, intentamos cargar .env.test
        env_file = base_dir / ".env.test"
        if env_file.exists():
            logger.info(f"Loading test environment from {env_file}")
            load_dotenv(env_file)
        else:
            logger.warning(f"Test environment file {env_file} not found, using default test values")
    else:
        # En otros entornos, cargamos el .env normal
        env_file = base_dir / ".env"
        if env_file.exists():
            logger.info(f"Loading environment from {env_file}")
            load_dotenv(env_file)
        else:
            logger.warning(f"Environment file {env_file} not found, using environment variables")


# Cargar variables de entorno
load_env_files()

# Obtener variables de configuración
supabase_url: str = os.getenv("SUPABASE_URL", "")
supabase_key: str = os.getenv("SUPABASE_KEY", "")

# Inicializar cliente como None para manejar errores
supabase_client: Client | None = None

# En entorno de prueba, usar valores por defecto si no están definidos
if "pytest" in sys.modules and (not supabase_url or not supabase_key):
    supabase_url = "https://example.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.mock-key-for-testing"
    logger.info("Using mock Supabase credentials for testing")
elif not supabase_url or not supabase_key:
    error_msg = "Missing SUPABASE_URL or SUPABASE_KEY environment variables"
    logger.error(error_msg)
    raise ValueError(error_msg)

# Crear cliente de Supabase
try:
    logger.debug(f"Creating Supabase client with URL: {supabase_url[:20]}...")
    supabase_client = create_client(supabase_url, supabase_key)
    logger.info("Supabase client created successfully")
except Exception as e:
    if "pytest" in sys.modules:
        # En pruebas, crear un mock del cliente
        supabase_client = MagicMock()
        logger.warning(f"Created mock Supabase client for testing. Error was: {e!s}")
    else:
        # En producción, propagar el error
        logger.error(f"Failed to create Supabase client: {e!s}")
        raise ValueError(f"Error creating Supabase client: {e!s}") from e
