#!/usr/bin/env python3
"""
Script para corregir problemas comunes en las pruebas.
Este script prepara el entorno para que las pruebas se ejecuten correctamente.
"""

import os
import subprocess
import sys
from pathlib import Path


def ensure_directory_exists(directory):
    """Asegura que un directorio existe."""
    os.makedirs(directory, exist_ok=True)
    print(f"✅ Directorio {directory} verificado")


def ensure_file_exists(file_path, content=""):
    """Asegura que un archivo existe."""
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Archivo {file_path} creado")
    else:
        print(f"✅ Archivo {file_path} verificado")


def install_dependencies(requirements_file, dev_requirements=None):
    """Instala las dependencias necesarias."""
    if os.path.exists(requirements_file):
        print(f"Instalando dependencias desde {requirements_file}...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", requirements_file], check=False
        )
        print("✅ Dependencias instaladas")
    else:
        print(f"⚠️ Archivo {requirements_file} no encontrado")

    if dev_requirements and os.path.exists(dev_requirements):
        print(f"Instalando dependencias de desarrollo desde {dev_requirements}...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", dev_requirements], check=False
        )
        print("✅ Dependencias de desarrollo instaladas")


def install_test_dependencies():
    """Instala las dependencias necesarias para las pruebas."""
    test_deps = ["pytest", "pytest-asyncio", "pytest-cov", "httpx"]
    print("Instalando dependencias de prueba...")
    subprocess.run([sys.executable, "-m", "pip", "install"] + test_deps, check=False)
    print("✅ Dependencias de prueba instaladas")


def create_test_env_file(env_file):
    """Crea un archivo .env para pruebas si no existe."""
    if not os.path.exists(env_file):
        content = """
# Archivo .env para pruebas
APP_ENV=testing
DEBUG=true
TESTING=true
DATABASE_URL=sqlite:///./test.db
SUPABASE_URL=https://example.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlc3QiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYxNjQxMjQ5MCwiZXhwIjoxOTMyMDEyNDkwfQ.fake-token-for-testing
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlc3QiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNjE2NDEyNDkwLCJleHAiOjE5MzIwMTI0OTB9.fake-service-key-for-testing
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+15551234567
REDIS_URL=redis://localhost:6379/0
"""
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Archivo {env_file} creado para pruebas")
    else:
        print(f"✅ Archivo {env_file} verificado")


def fix_conftest_if_needed(conftest_path):
    """Corrige el archivo conftest.py si es necesario."""
    if not os.path.exists(conftest_path):
        content = """
import pytest
import os
import sys

# Asegurarse de que el directorio raíz del proyecto esté en el path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configurar variables de entorno para pruebas
os.environ["APP_ENV"] = "testing"
os.environ["TESTING"] = "true"
os.environ["DEBUG"] = "true"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def event_loop():
    # Create an instance of the default event loop for each test case.
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
"""
        with open(conftest_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Archivo {conftest_path} creado")
    else:
        print(f"✅ Archivo {conftest_path} verificado")


def main():
    """Función principal."""
    print("🔧 Preparando entorno para pruebas...")

    # Obtener el directorio raíz del proyecto
    root_dir = Path(__file__).parent.parent.absolute()
    backend_dir = root_dir / "backend-call-automation"
    frontend_dir = root_dir / "frontend-call-automation"

    # Verificar directorios necesarios
    ensure_directory_exists(backend_dir / "logs")
    ensure_directory_exists(backend_dir / "tests")

    # Verificar archivos necesarios
    ensure_file_exists(backend_dir / "logs" / "app.log")

    # Instalar dependencias
    install_dependencies(backend_dir / "requirements.txt", backend_dir / "requirements-dev.txt")
    install_test_dependencies()

    # Crear archivo .env para pruebas
    create_test_env_file(backend_dir / ".env.test")

    # Corregir conftest.py si es necesario
    fix_conftest_if_needed(backend_dir / "tests" / "conftest.py")

    print("✅ Entorno preparado para pruebas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
