#!/usr/bin/env python3
import subprocess
import sys
from typing import List, Tuple
import os


def run_command(command: List[str]) -> Tuple[int, str]:
    """Ejecuta un comando y retorna el código de salida y la salida."""
    process = subprocess.run(command, capture_output=True, text=True, shell=True)
    return process.returncode, process.stdout


def check_python_files() -> bool:
    """Verifica la calidad de archivos Python."""
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
    """Verifica la calidad de archivos TypeScript."""
    print("🔍 Verificando archivos TypeScript...")

    os.chdir("frontend-call-automation")

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


def main() -> int:
    """Función principal de auditoría."""
    print("🚀 Iniciando auditoría de calidad...")

    success = True
    if not check_python_files():
        success = False
    if not check_typescript_files():
        success = False

    if success:
        print("✅ Auditoría completada exitosamente")
        return 0
    else:
        print("❌ Se encontraron problemas durante la auditoría")
        return 1


if __name__ == "__main__":
    sys.exit(main())
