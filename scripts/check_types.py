#!/usr/bin/env python3
"""
Script para verificar los tipos en el proyecto usando mypy.
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Ejecuta mypy en el proyecto."""
    # Obtener el directorio raíz del proyecto
    root_dir = Path(__file__).parent.parent.absolute()
    
    # Directorios a verificar
    dirs_to_check = [
        "app",
        "tests",
    ]
    
    # Construir el comando de mypy
    cmd = ["mypy"]
    for dir_name in dirs_to_check:
        dir_path = root_dir / dir_name
        if dir_path.exists():
            cmd.append(str(dir_path))
    
    # Ejecutar mypy
    print(f"Ejecutando: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Mostrar la salida
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    # Devolver el código de salida
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
