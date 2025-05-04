#!/usr/bin/env python
"""
Script para verificar la validez de los archivos RST en el proyecto.

Este script utiliza docutils para verificar la sintaxis de los archivos RST
y generar un informe con los errores encontrados.
"""

import argparse
import os
import sys

from docutils.core import publish_string


def check_rst_file(file_path: str) -> list[str]:
    """
    Verifica un archivo RST y devuelve una lista de errores.

    Args:
        file_path: Ruta al archivo RST a verificar

    Returns:
        Lista de mensajes de error
    """
    errors = []

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Configurar docutils para capturar errores
        settings_overrides = {
            "halt_level": 5,  # No detener en ningún nivel de error
            "report_level": 1,  # Reportar todos los mensajes
            "warning_stream": None,  # No imprimir advertencias
        }

        try:
            # Intentar procesar el archivo RST
            publish_string(
                content,
                writer_name="null",
                settings_overrides=settings_overrides,
            )
        except Exception as e:
            # Capturar errores de docutils
            errors.append(str(e))

    except Exception as e:
        errors.append(f"Error al leer el archivo: {e}")

    return errors


def find_rst_files(directory: str, exclude_dirs: set[str]) -> list[str]:
    """
    Encuentra todos los archivos RST en un directorio y sus subdirectorios.

    Args:
        directory: Directorio a buscar
        exclude_dirs: Conjunto de directorios a excluir

    Returns:
        Lista de rutas a archivos RST
    """
    rst_files = []

    for root, dirs, files in os.walk(directory):
        # Excluir directorios
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            if file.endswith(".rst"):
                rst_files.append(os.path.join(root, file))

    return rst_files


def generate_report(results: list[tuple[str, list[str]]], output_file: str | None = None) -> None:
    """
    Genera un informe con los errores encontrados en los archivos RST.

    Args:
        results: Lista de tuplas (ruta_archivo, lista_errores)
        output_file: Archivo de salida (opcional)
    """
    output = []
    output.append("Informe de Verificación de Archivos RST")
    output.append("======================================\n")

    total_files = len(results)
    files_with_errors = sum(1 for _, errors in results if errors)

    for file_path, errors in results:
        rel_path = os.path.relpath(file_path)

        if errors:
            output.append(f"Archivo: {rel_path}")
            output.append("-" * (len(rel_path) + 9))

            for error in errors:
                output.append(f"  - {error}")

            output.append("")
        else:
            output.append(f"Archivo: {rel_path} - Sin errores")
            output.append("")

    output.append("Resumen")
    output.append("=======")
    output.append(f"Total de archivos verificados: {total_files}")
    output.append(f"Archivos con errores: {files_with_errors}")
    output.append(f"Archivos sin errores: {total_files - files_with_errors}")

    report = "\n".join(output)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Informe guardado en {output_file}")
    else:
        print(report)


def main() -> int:
    """Función principal del script."""
    parser = argparse.ArgumentParser(description="Verificar archivos RST")
    parser.add_argument("--directory", "-d", default=".", help="Directorio a verificar")
    parser.add_argument("--output", "-o", help="Archivo de salida para el informe")
    parser.add_argument(
        "--exclude",
        "-e",
        nargs="+",
        default=["venv", ".venv", "__pycache__", "_build"],
        help="Directorios a excluir",
    )

    args = parser.parse_args()

    try:
        import docutils
    except ImportError:
        print("Error: docutils no está instalado. Instálelo con 'pip install docutils'")
        return 1

    exclude_dirs = set(args.exclude)
    rst_files = find_rst_files(args.directory, exclude_dirs)

    if not rst_files:
        print(f"No se encontraron archivos RST en {args.directory}")
        return 0

    results = []
    for file_path in rst_files:
        errors = check_rst_file(file_path)
        results.append((file_path, errors))

    generate_report(results, args.output)

    # Devolver código de salida 1 si hay archivos con errores
    return 1 if any(errors for _, errors in results) else 0


if __name__ == "__main__":
    sys.exit(main())
