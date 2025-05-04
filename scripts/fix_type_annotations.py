#!/usr/bin/env python
"""
Script para corregir automáticamente problemas comunes de anotaciones de tipo.

Este script busca patrones comunes de problemas de tipos y los corrige
automáticamente en los archivos Python del proyecto.
"""

import argparse
import os
import re
import sys


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
        # Excluir directorios
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    return python_files


def fix_missing_init_return_type(content: str) -> str:
    """
    Corrige las anotaciones de tipo faltantes en los métodos __init__.

    Args:
        content: Contenido del archivo

    Returns:
        Contenido corregido
    """
    # Patrón para encontrar métodos __init__ sin anotación de tipo de retorno
    pattern = re.compile(r"(\s+def __init__\([^)]*\))(:)(\s*)")

    # Reemplazar con anotación de tipo de retorno None
    return pattern.sub(r"\1 -> None\3", content)


def fix_missing_return_none(content: str) -> str:
    """
    Corrige las anotaciones de tipo faltantes en funciones que deberían devolver None.

    Args:
        content: Contenido del archivo

    Returns:
        Contenido corregido
    """
    # Patrón para encontrar funciones que no devuelven nada y no tienen anotación de tipo
    pattern = re.compile(r'(\s+def\s+\w+\([^)]*\))(:)(\s*""")')

    # Reemplazar con anotación de tipo de retorno None
    return pattern.sub(r"\1 -> None\3", content)


def fix_missing_function_arg_types(content: str) -> str:
    """
    Corrige las anotaciones de tipo faltantes en argumentos de funciones.

    Args:
        content: Contenido del archivo

    Returns:
        Contenido corregido
    """
    # Este es un caso más complejo que requeriría un análisis AST completo
    # Por ahora, solo identificamos casos simples

    # Patrón para encontrar argumentos sin tipo en funciones
    pattern = re.compile(r"(\s+def\s+\w+\()([^:)]+)(\))")

    def add_any_type(match: re.Match) -> str:
        args = match.group(2).split(",")
        typed_args = []

        for arg in args:
            arg = arg.strip()
            if arg and ":" not in arg and arg != "self" and arg != "cls":
                typed_args.append(f"{arg}: Any")
            else:
                typed_args.append(arg)

        return f"{match.group(1)}{', '.join(typed_args)}{match.group(3)}"

    return pattern.sub(add_any_type, content)


def fix_implicit_optional(content: str) -> str:
    """
    Corrige los parámetros opcionales implícitos.

    Args:
        content: Contenido del archivo

    Returns:
        Contenido corregido
    """
    # Patrón para encontrar parámetros con valor predeterminado None sin Optional
    pattern = re.compile(r"(\s+)(\w+):\s+([^=\s]+)\s+=\s+None")

    # Reemplazar con Optional[tipo]
    return pattern.sub(r"\1\2: Optional[\3] = None", content)


def fix_file(file_path: str, dry_run: bool = False) -> tuple[int, list[str]]:
    """
    Corrige problemas de tipos en un archivo.

    Args:
        file_path: Ruta al archivo a corregir
        dry_run: Si es True, no se realizan cambios en el archivo

    Returns:
        Tupla con el número de correcciones y lista de correcciones realizadas
    """
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    original_content = content
    corrections = []

    # Verificar si necesitamos importar Optional y Any
    needs_optional = "Optional" not in content and "= None" in content
    needs_any = "Any" not in content

    # Añadir importaciones si es necesario
    if needs_optional or needs_any:
        imports_to_add = []
        if needs_optional:
            imports_to_add.append("Optional")
        if needs_any:
            imports_to_add.append("Any")

        if imports_to_add:
            import_str = f"from typing import {', '.join(imports_to_add)}"

            # Buscar dónde añadir la importación
            if "from typing import " in content:
                # Añadir a una importación existente
                pattern = re.compile(r"from typing import ([^\n]+)")

                def add_imports(match: re.Match) -> str:
                    existing_imports = match.group(1).strip()
                    for imp in imports_to_add:
                        if imp not in existing_imports:
                            existing_imports += f", {imp}"
                    return f"from typing import {existing_imports}"

                new_content = pattern.sub(add_imports, content)
                if new_content != content:
                    content = new_content
                    corrections.append(
                        f"Añadida importación de typing: {', '.join(imports_to_add)}"
                    )
            else:
                # Añadir una nueva línea de importación después de las importaciones existentes
                import_pattern = re.compile(r"((?:import|from)\s+[^\n]+\n+)")
                last_import = list(import_pattern.finditer(content))

                if last_import:
                    last_pos = last_import[-1].end()
                    content = content[:last_pos] + import_str + "\n\n" + content[last_pos:]
                    corrections.append(f"Añadida importación: {import_str}")
                else:
                    # No hay importaciones, añadir al principio del archivo
                    content = import_str + "\n\n" + content
                    corrections.append(f"Añadida importación: {import_str}")

    # Aplicar correcciones
    new_content = fix_missing_init_return_type(content)
    if new_content != content:
        content = new_content
        corrections.append("Corregidas anotaciones de tipo en métodos __init__")

    new_content = fix_missing_return_none(content)
    if new_content != content:
        content = new_content
        corrections.append("Corregidas anotaciones de tipo en funciones que devuelven None")

    new_content = fix_implicit_optional(content)
    if new_content != content:
        content = new_content
        corrections.append("Corregidos parámetros opcionales implícitos")

    # No aplicamos fix_missing_function_arg_types por defecto porque puede ser demasiado agresivo

    # Guardar cambios si es necesario
    if content != original_content and not dry_run:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    return len(corrections), corrections


def main() -> int:
    """Función principal del script."""
    parser = argparse.ArgumentParser(
        description="Corregir problemas comunes de anotaciones de tipo"
    )
    parser.add_argument(
        "--directory", "-d", default="backend-call-automation", help="Directorio a procesar"
    )
    parser.add_argument(
        "--exclude",
        "-e",
        nargs="+",
        default=["venv", ".venv", "__pycache__", "migrations", "tests"],
        help="Directorios a excluir",
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="No realizar cambios, solo mostrar qué se haría",
    )

    args = parser.parse_args()

    exclude_dirs = set(args.exclude)
    python_files = find_python_files(args.directory, exclude_dirs)

    total_corrections = 0
    files_corrected = 0

    for file_path in python_files:
        num_corrections, corrections = fix_file(file_path, args.dry_run)

        if num_corrections > 0:
            files_corrected += 1
            total_corrections += num_corrections

            print(f"Archivo: {file_path}")
            for correction in corrections:
                print(f"  - {correction}")
            print()

    print("Resumen:")
    print(f"- Archivos procesados: {len(python_files)}")
    print(f"- Archivos corregidos: {files_corrected}")
    print(f"- Total de correcciones: {total_corrections}")

    if args.dry_run:
        print("\nEjecutado en modo simulación. No se realizaron cambios reales.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
