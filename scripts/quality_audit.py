#!/usr/bin/env python3
"""
Script para auditar la calidad del código en el proyecto.

Este script verifica la calidad de los archivos Python y TypeScript,
comprobando imports no utilizados, complejidad ciclomática, cobertura de tipos,
y reglas de linting.
"""

import os
import subprocess
import sys


def run_command(command: list[str]) -> tuple[int, str]:
    """
    Ejecuta un comando y retorna el código de salida y la salida.

    Args:
        command: Lista de strings que representan el comando a ejecutar.

    Returns:
        Tupla con el código de salida y la salida del comando.
    """
    # Usar shell=False para evitar problemas de seguridad
    # Validar que todos los elementos del comando sean strings
    if not all(isinstance(arg, str) for arg in command):
        raise ValueError("Todos los argumentos del comando deben ser cadenas de texto.")

    # Validar que los argumentos no contengan caracteres potencialmente peligrosos
    for arg in command:
        if any(char in arg for char in [";", "&", "|", "`"]):
            raise ValueError(f"El argumento '{arg}' contiene caracteres no permitidos.")

    process = subprocess.run(command, capture_output=True, text=True, shell=False, check=False)
    return process.returncode, process.stdout


def check_python_files() -> bool:
    """
    Verifica la calidad de archivos Python.

    Returns:
        bool: True si todas las verificaciones pasan, False en caso contrario.
    """
    print("🔍 Verificando archivos Python...")

    # Verificar imports no utilizados
    code, output = run_command(["ruff", "check", ".", "--select", "F401"])
    if code != 0:
        print("❌ Se encontraron imports no utilizados:")
        print(output)
        return False

    # Verificar complejidad ciclomática
    code, output = run_command(["ruff", "check", ".", "--select", "C901"])
    if code != 0:
        print("❌ Funciones con alta complejidad detectadas:")
        print(output)
        return False

    # Verificar cobertura de tipos
    code, output = run_command(["mypy", "."])
    if code != 0:
        print("❌ Problemas con tipos detectados:")
        print(output)
        return False

    return True


def check_typescript_files() -> bool:
    """
    Verifica la calidad de archivos TypeScript.

    Returns:
        bool: True si todas las verificaciones pasan, False en caso contrario.
    """
    print("🔍 Verificando archivos TypeScript...")

    # Guardar el directorio actual
    current_dir = os.getcwd()

    try:
        # Cambiar al directorio frontend
        if os.path.exists("frontend-call-automation"):
            os.chdir("frontend-call-automation")
        else:
            print("❌ No se encontró el directorio frontend-call-automation")
            return False

        # Verificar reglas de ESLint
        code, output = run_command(["npm", "run", "lint", "--", "--max-warnings", "0"])
        if code != 0:
            print("❌ Problemas de linting detectados:")
            print(output)
            return False

        # Verificar tipos TypeScript
        code, output = run_command(["npm", "run", "type-check"])
        if code != 0:
            print("❌ Problemas de tipos TypeScript detectados:")
            print(output)
            return False

        return True
    finally:
        # Asegurarse de volver al directorio original
        os.chdir(current_dir)


def main() -> int:
    """
    Función principal de auditoría.

    Returns:
        int: 0 si la auditoría es exitosa, 1 si hay problemas.
    """
    print("🚀 Iniciando auditoría de calidad...")

    success = True
    if not check_python_files():
        success = False
    if not check_typescript_files():
        success = False

    if success:
        print("✅ Auditoría completada exitosamente")
        return 0
    print("❌ Se encontraron problemas durante la auditoría")
    return 1


if __name__ == "__main__":
    sys.exit(main())
