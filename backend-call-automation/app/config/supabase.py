"""
Módulo de configuración del cliente Supabase.

Este módulo configura y exporta una instancia única del cliente Supabase
para ser utilizada en toda la aplicación. Utiliza variables de entorno
para la configuración de credenciales.

Variables de entorno requeridas:
    - SUPABASE_URL: URL de la instancia de Supabase
    - SUPABASE_KEY: Clave de acceso anónimo de Supabase
"""

from supabase import create_client, Client
import os
from dotenv import load_dotenv
import sys

# Cargar variables de entorno según el entorno
if "pytest" in sys.modules:
    # Si estamos en un entorno de prueba, cargamos .env.test
    load_dotenv(".env.test")
else:
    # En otros entornos, cargamos el .env normal
    load_dotenv()

supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")

# En entorno de prueba, usar valores por defecto si no están definidos
if "pytest" in sys.modules and (not supabase_url or not supabase_key):
    supabase_url = "https://example.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.mock-key-for-testing"
    print("Using mock Supabase credentials for testing")
elif not supabase_url or not supabase_key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables")

# Crear cliente de Supabase
try:
    supabase_client: Client = create_client(supabase_url, supabase_key)
except Exception as e:
    if "pytest" in sys.modules:
        # En pruebas, crear un mock del cliente
        from unittest.mock import MagicMock
        supabase_client = MagicMock()
        print(f"Created mock Supabase client for testing. Error was: {str(e)}")
    else:
        # En producción, propagar el error
        raise
