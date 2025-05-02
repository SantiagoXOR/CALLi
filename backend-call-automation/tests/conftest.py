import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Configurar PYTHONPATH para asegurar que las importaciones funcionen correctamente
# Esto es crucial para resolver problemas como "ModuleNotFoundError: No module named 'app.dependencies'"

# 1. Agregar el directorio raíz del proyecto al PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 2. Agregar el directorio padre del backend-call-automation al PYTHONPATH (si existe)
parent_dir = project_root.parent
if parent_dir.exists():
    sys.path.insert(0, str(parent_dir))

# 3. Imprimir información de depuración sobre el PYTHONPATH
print(f"PYTHONPATH configurado para tests:")
print(f"- Directorio actual: {os.getcwd()}")
print(f"- Directorio del proyecto: {project_root}")
print(f"- sys.path: {sys.path[:5]}")  # Mostrar solo los primeros 5 elementos para brevedad

# Establecer variables de entorno críticas para el entorno de prueba
# Estas variables deben definirse ANTES de importar cualquier módulo de la aplicación que las utilice
os.environ["TESTING"] = "1"
os.environ["APP_ENV"] = "testing"
# Usar claves de API de prueba o mocks; no usar claves reales en las pruebas
os.environ["OPENAI_API_KEY"] = "test_openai_api_key"
os.environ["ELEVENLABS_API_KEY"] = "test_elevenlabs_api_key"
# Configurar otras variables de entorno necesarias para las pruebas
os.environ["DATABASE_URL"] = "test_database_url"
os.environ["SUPABASE_URL"] = "test_supabase_url"
os.environ["SUPABASE_KEY"] = "test_supabase_key"
os.environ["SUPABASE_SERVICE_KEY"] = "test_supabase_service_key"
os.environ["TWILIO_ACCOUNT_SID"] = "test_twilio_account_sid"
os.environ["TWILIO_AUTH_TOKEN"] = "test_twilio_auth_token"
os.environ["TWILIO_PHONE_NUMBER"] = "test_twilio_phone_number"
os.environ["APP_NAME"] = "test_app_name"
os.environ["APP_DEBUG"] = "True"
os.environ["APP_URL"] = "test_app_url"
os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["ALGORITHM"] = "test_algorithm"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["HOST"] = "test_host"
os.environ["PORT"] = "8000"
os.environ["DEBUG"] = "True"
os.environ["ENVIRONMENT"] = "testing"
# Añadir variables de Vault si son necesarias para las pruebas, aunque secrets_manager debería ser mockeado
os.environ["VAULT_ADDR"] = "http://mock-vault:8200"
os.environ["VAULT_TOKEN"] = "mock_vault_token"

# Importar configuraciones y servicios DESPUÉS de establecer las variables de entorno
from app.config.settings import Settings


@pytest.fixture(scope="session", autouse=True)
def mock_settings():
    """
    Fixture que proporciona configuraciones mock para todas las pruebas.
    Se aplica automáticamente a todas las pruebas de la sesión.
    """
    # Usar patch para mockear la clase Settings completa o la función get_settings
    # Esto evita que Pydantic intente cargar y validar desde el entorno real durante las pruebas
    with patch("app.config.settings.Settings", spec=Settings) as MockSettings:
        mock_instance = MockSettings.return_value
        # Configurar valores mock para los atributos de settings necesarios en las pruebas
        mock_instance.ELEVENLABS_MAX_CONNECTIONS = 10
        mock_instance.ELEVENLABS_POOL_TIMEOUT = 30
        mock_instance.ELEVENLABS_MAX_RETRIES = 3
        # Asegurarse de que otras configuraciones necesarias también estén mockeadas
        mock_instance.DATABASE_URL = os.environ["DATABASE_URL"]
        mock_instance.SUPABASE_URL = os.environ["SUPABASE_URL"]
        mock_instance.SUPABASE_KEY = os.environ["SUPABASE_KEY"]
        mock_instance.SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
        mock_instance.TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
        mock_instance.TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
        mock_instance.TWILIO_PHONE_NUMBER = os.environ["TWILIO_PHONE_NUMBER"]
        mock_instance.APP_NAME = os.environ["APP_NAME"]
        mock_instance.APP_ENV = os.environ["APP_ENV"]
        mock_instance.APP_DEBUG = os.environ["APP_DEBUG"] == "True"
        mock_instance.APP_URL = os.environ["APP_URL"]
        mock_instance.SECRET_KEY = os.environ["SECRET_KEY"]
        mock_instance.ALGORITHM = os.environ["ALGORITHM"]
        mock_instance.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
        mock_instance.HOST = os.environ["HOST"]
        mock_instance.PORT = int(os.environ["PORT"])
        mock_instance.DEBUG = os.environ["DEBUG"] == "True"
        mock_instance.ENVIRONMENT = os.environ["ENVIRONMENT"]
        yield mock_instance  # Devolver la instancia mockeada para que esté disponible si se necesita explícitamente


# Nota: La fixture elevenlabs_service y las pruebas se movieron a test_elevenlabs_service.py
# Este archivo conftest.py ahora se enfoca en la configuración global del entorno de prueba.
