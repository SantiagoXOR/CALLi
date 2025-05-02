#!/usr/bin/env python3
"""
Script para impedir la creación de workflows prohibidos.
"""

import os
import sys

# Lista de workflows prohibidos
PROHIBITED_WORKFLOWS = [
    "ci-cd-pipeline.yml",
    "config-security-scan.yml",
]


def main():
    """
    Verifica si alguno de los archivos pasados como argumento es un workflow prohibido.
    """
    # Obtener la lista de archivos a verificar
    files_to_check = sys.argv[1:]

    # Verificar cada archivo
    for file_path in files_to_check:
        # Obtener el nombre del archivo
        file_name = os.path.basename(file_path)

        # Verificar si el archivo está en la lista de workflows prohibidos
        if file_name in PROHIBITED_WORKFLOWS:
            print(f"ERROR: No se permite añadir el archivo {file_name}")
            print(
                "Este archivo ha sido eliminado permanentemente debido a problemas persistentes."
            )
            print(
                "Por favor, consulta .github/workflows/README.md para más información."
            )
            sys.exit(1)

    # Si llegamos aquí, todos los archivos son válidos
    sys.exit(0)


if __name__ == "__main__":
    main()
