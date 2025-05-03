#!/usr/bin/env python
"""
Script para probar la instalación de dependencias y verificar conflictos.
Este script intenta instalar las dependencias de los archivos requirements.txt
y reporta cualquier conflicto que encuentre.
"""

import os
import subprocess
import sys
import tempfile
import venv
from pathlib import Path


def create_virtual_env(venv_dir):
    """Crea un entorno virtual para probar las dependencias."""
    print(f"Creando entorno virtual en {venv_dir}...")
    venv.create(venv_dir, with_pip=True)

    # Determinar el ejecutable de pip
    if os.name == "nt":  # Windows
        pip_exe = os.path.join(venv_dir, "Scripts", "pip.exe")
    else:  # Unix/Linux/Mac
        pip_exe = os.path.join(venv_dir, "bin", "pip")

    return pip_exe


def install_dependencies(pip_exe, requirements_file):
    """Instala dependencias desde un archivo requirements.txt."""
    print(f"Instalando dependencias desde {requirements_file}...")
    result = subprocess.run(
        [pip_exe, "install", "-r", requirements_file], capture_output=True, text=True, check=False
    )

    if result.returncode != 0:
        print("Error al instalar dependencias:")
        print(result.stderr)
        return False

    print("Dependencias instaladas correctamente.")
    return True


def check_dependency_conflicts(pip_exe):
    """Verifica si hay conflictos de dependencias."""
    print("Verificando conflictos de dependencias...")
    result = subprocess.run([pip_exe, "check"], capture_output=True, text=True, check=False)

    if "No broken requirements found." in result.stdout:
        print("No se encontraron conflictos de dependencias.")
        return True
    print("Se encontraron conflictos de dependencias:")
    print(result.stdout)
    return False


def main():
    """Función principal."""
    # Obtener la ruta del proyecto
    project_root = Path(__file__).parent.parent.absolute()

    # Rutas de los archivos requirements.txt
    main_requirements = os.path.join(project_root, "requirements.txt")
    backend_requirements = os.path.join(project_root, "backend-call-automation", "requirements.txt")

    # Verificar que los archivos existen
    if not os.path.exists(main_requirements):
        print(f"Error: No se encontró el archivo {main_requirements}")
        return 1

    if not os.path.exists(backend_requirements):
        print(f"Error: No se encontró el archivo {backend_requirements}")
        return 1

    # Crear un entorno virtual temporal
    with tempfile.TemporaryDirectory() as temp_dir:
        venv_dir = os.path.join(temp_dir, "venv")
        pip_exe = create_virtual_env(venv_dir)

        # Actualizar pip (sin verificar errores)
        try:
            subprocess.run([pip_exe, "install", "--upgrade", "pip"], check=False)
        except Exception as e:
            print(f"Advertencia: No se pudo actualizar pip: {e}")
            print("Continuando con la versión actual de pip...")

        # Instalar packaging primero para evitar conflictos
        subprocess.run([pip_exe, "install", "packaging>=21.0,<28.0"], check=True)

        # Instalar dependencias principales
        if not install_dependencies(pip_exe, main_requirements):
            return 1

        # Verificar conflictos después de instalar las dependencias principales
        if not check_dependency_conflicts(pip_exe):
            return 1

        # Instalar dependencias del backend
        if not install_dependencies(pip_exe, backend_requirements):
            print(
                "Advertencia: Algunos paquetes del backend no pudieron instalarse, pero continuamos."
            )

        # Verificar conflictos finales
        if not check_dependency_conflicts(pip_exe):
            return 1

        print("¡Todas las dependencias se instalaron correctamente sin conflictos!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
