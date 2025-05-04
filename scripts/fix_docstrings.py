#!/usr/bin/env python3
"""
Script para verificar y corregir docstrings en el proyecto.

Este script verifica que todas las funciones, clases y módulos tengan docstrings
adecuados y sugiere correcciones para los que faltan.
"""

import ast
import os
import sys


def check_docstrings(filename: str) -> list[dict[str, str]]:
    """
    Verifica docstrings en un archivo Python.

    Args:
        filename: Ruta al archivo Python a verificar

    Returns:
        Lista de diccionarios con información sobre docstrings faltantes
    """
    with open(filename, encoding="utf-8") as file:
        content = file.read()

    errors = []
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return [{"type": "syntax_error", "name": filename, "message": str(e)}]

    # Verificar docstring del módulo
    if not ast.get_docstring(tree):
        errors.append(
            {
                "type": "module",
                "name": filename,
                "message": f"Missing module docstring in {filename}",
                "lineno": 1,
            }
        )

    # Verificar clases y funciones
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            # Omitir métodos/funciones privados (que comienzan con _)
            if node.name.startswith("_") and node.name != "__init__":
                continue

            docstring = ast.get_docstring(node)
            if not docstring:
                errors.append(
                    {
                        "type": node.__class__.__name__,
                        "name": node.name,
                        "message": f"Missing docstring for {node.__class__.__name__} '{node.name}' in {filename}",
                        "lineno": node.lineno,
                        "args": [arg.arg for arg in node.args.args]
                        if hasattr(node, "args")
                        else [],
                        "returns": node.returns is not None if hasattr(node, "returns") else False,
                    }
                )
            elif docstring and isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Verificar secciones del docstring de la función
                missing_sections = []

                # Verificar sección Args
                if (
                    "Args:" not in docstring
                    and "Parameters:" not in docstring
                    and len(node.args.args) > 1
                ):
                    # El primer arg podría ser self/cls, así que solo advertir si hay más de 1 arg
                    missing_sections.append("Args")

                # Verificar sección Returns
                if "Returns:" not in docstring and node.returns:
                    missing_sections.append("Returns")

                if missing_sections:
                    errors.append(
                        {
                            "type": "incomplete_docstring",
                            "name": node.name,
                            "message": f"Function '{node.name}' in {filename} is missing sections: {', '.join(missing_sections)}",
                            "lineno": node.lineno,
                            "missing_sections": missing_sections,
                            "args": [arg.arg for arg in node.args.args]
                            if hasattr(node, "args")
                            else [],
                            "returns": node.returns is not None
                            if hasattr(node, "returns")
                            else False,
                        }
                    )

    return errors


def generate_docstring_template(error: dict[str, str]) -> str:
    """
    Genera una plantilla de docstring basada en el tipo de error.

    Args:
        error: Diccionario con información sobre el error de docstring

    Returns:
        Plantilla de docstring generada
    """
    if error["type"] == "module":
        return '"""Descripción del módulo."""\n'

    if error["type"] == "ClassDef":
        return '"""Descripción de la clase."""\n'

    if error["type"] in ["FunctionDef", "AsyncFunctionDef"]:
        template = '"""Descripción de la función.\n\n'

        # Agregar sección Args si hay argumentos
        args = error.get("args", [])
        if len(args) > 0:
            template += "Args:\n"
            for arg in args:
                if arg in ["self", "cls"]:
                    continue
                template += f"    {arg}: Descripción del parámetro\n"
            template += "\n"

        # Agregar sección Returns si la función tiene anotación de retorno
        if error.get("returns", False):
            template += "Returns:\n    Descripción del valor de retorno\n"

        template += '"""'
        return template

    if error["type"] == "incomplete_docstring":
        template = "Secciones faltantes:\n"

        if "Args" in error.get("missing_sections", []):
            template += "\nArgs:\n"
            for arg in error.get("args", []):
                if arg in ["self", "cls"]:
                    continue
                template += f"    {arg}: Descripción del parámetro\n"

        if "Returns" in error.get("missing_sections", []):
            template += "\nReturns:\n    Descripción del valor de retorno\n"

        return template

    return "No se pudo generar una plantilla para este tipo de error."


def find_python_files(directory: str, exclude_dirs: set[str]) -> list[str]:
    """
    Encuentra todos los archivos Python en un directorio y sus subdirectorios.

    Args:
        directory: Directorio a buscar
        exclude_dirs: Conjunto de directorios a excluir

    Returns:
        Lista de rutas a archivos Python
    """
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Excluir directorios no deseados
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    return python_files


def main() -> int:
    """
    Función principal.

    Returns:
        Código de salida (0 si no hay errores, 1 si hay errores)
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Verificar y corregir docstrings en archivos Python"
    )
    parser.add_argument(
        "--directory", "-d", default="backend-call-automation", help="Directorio a verificar"
    )
    parser.add_argument("--output", "-o", help="Archivo de salida para el informe")
    parser.add_argument(
        "--fix", "-f", action="store_true", help="Generar plantillas para docstrings faltantes"
    )
    args = parser.parse_args()

    # Directorios a excluir
    exclude_dirs = {
        "__pycache__",
        ".git",
        ".github",
        ".vscode",
        ".idea",
        "venv",
        ".venv",
        "env",
        ".env",
        "node_modules",
        "dist",
        "build",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
    }

    # Encontrar archivos Python
    python_files = find_python_files(args.directory, exclude_dirs)

    # Verificar docstrings
    all_errors = []
    for file in python_files:
        errors = check_docstrings(file)
        all_errors.extend(errors)

    # Ordenar errores por archivo y línea
    all_errors.sort(key=lambda e: (e.get("name", ""), e.get("lineno", 0)))

    # Generar informe
    report = []
    report.append(f"Docstring Check Report - {len(all_errors)} issues found\n")
    report.append("=" * 80 + "\n")

    current_file = None
    for error in all_errors:
        if current_file != error.get("name"):
            current_file = error.get("name")
            report.append(f"\nFile: {current_file}\n")
            report.append("-" * 80 + "\n")

        report.append(f"Line {error.get('lineno', '?')}: {error['message']}\n")

        if args.fix:
            template = generate_docstring_template(error)
            report.append("Suggested template:\n")
            for line in template.split("\n"):
                report.append(f"    {line}\n")
            report.append("\n")

    # Escribir informe
    report_text = "".join(report)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report_text)
        print(f"Report written to {args.output}")
    else:
        print(report_text)

    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())
