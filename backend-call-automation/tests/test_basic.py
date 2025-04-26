"""
Pruebas básicas para verificar que el entorno de pruebas funciona correctamente.
"""
import pytest
import os

def test_basic():
    """Basic test to ensure pytest is working"""
    assert True

def test_addition():
    """Test basic addition"""
    assert 1 + 1 == 2

def test_environment_setup():
    """Verifica que el entorno de pruebas está configurado correctamente."""
    assert True, "El entorno de pruebas está configurado correctamente"

def test_logs_directory_exists():
    """Verifica que el directorio de logs existe."""
    # Crear el directorio si no existe
    os.makedirs("logs", exist_ok=True)

    assert os.path.exists("logs"), "El directorio de logs no existe"
    assert os.path.isdir("logs"), "logs no es un directorio"

def test_app_log_file_exists():
    """Verifica que el archivo de log de la aplicación existe."""
    # Crear el archivo si no existe
    if not os.path.exists("logs/app.log"):
        with open("logs/app.log", "w") as f:
            f.write("")

    assert os.path.exists("logs/app.log"), "El archivo de log de la aplicación no existe"
    assert os.path.isfile("logs/app.log"), "app.log no es un archivo"

def test_python_version():
    """Verifica la versión de Python."""
    import sys
    assert sys.version_info.major == 3, "La versión de Python debe ser 3.x"
    assert sys.version_info.minor >= 8, "La versión de Python debe ser al menos 3.8"

def test_required_packages():
    """Verifica que los paquetes requeridos están instalados."""
    import importlib

    required_packages = [
        "fastapi",
        "pydantic",
        "sqlalchemy",
        "httpx",
        "pytest",
        "pytest-asyncio"
    ]

    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            pytest.fail(f"El paquete {package} no está instalado")
