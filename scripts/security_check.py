#!/usr/bin/env python3
"""
Script para verificar la configuración de seguridad del proyecto CALLi.
Este script realiza verificaciones básicas de seguridad en el código y la configuración.
"""

import os
import re
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple


# Colores para la salida en terminal
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def print_header(text: str) -> None:
    """Imprime un encabezado formateado."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}=== {text} ==={Colors.ENDC}\n")


def print_result(name: str, status: bool, message: str = "") -> None:
    """Imprime el resultado de una verificación."""
    status_text = (
        f"{Colors.GREEN}✓ PASS{Colors.ENDC}"
        if status
        else f"{Colors.RED}✗ FAIL{Colors.ENDC}"
    )
    print(f"{status_text} {name}")
    if message and not status:
        print(f"  {Colors.YELLOW}→ {message}{Colors.ENDC}")


def check_file_exists(path: str) -> bool:
    """Verifica si un archivo existe."""
    return os.path.isfile(path)


def check_file_content(file_path: str, pattern: str) -> bool:
    """Verifica si un archivo contiene un patrón específico."""
    if not os.path.isfile(file_path):
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        return bool(re.search(pattern, content))


def check_env_files() -> Tuple[bool, str]:
    """Verifica los archivos .env en busca de problemas de seguridad."""
    env_files = list(Path(".").glob("**/.env*"))
    example_files = [f for f in env_files if "example" in f.name.lower()]
    actual_env_files = [f for f in env_files if "example" not in f.name.lower()]

    if not example_files:
        return False, "No se encontraron archivos .env.example para referencia"

    if not actual_env_files:
        return True, "No se encontraron archivos .env reales (esto es bueno para CI)"

    # Verificar que los archivos .env no estén en el control de versiones
    try:
        git_files = subprocess.check_output(["git", "ls-files"], text=True).splitlines()
        tracked_env_files = [f for f in actual_env_files if str(f) in git_files]

        if tracked_env_files:
            return (
                False,
                f"Los siguientes archivos .env están en control de versiones: {', '.join(str(f) for f in tracked_env_files)}",
            )
    except subprocess.SubprocessError:
        pass  # Ignorar si git no está disponible

    return True, ""


def check_security_headers() -> Tuple[bool, str]:
    """Verifica los encabezados de seguridad en la configuración de nginx."""
    nginx_conf = "nginx/conf.d/default.conf"
    if not os.path.isfile(nginx_conf):
        return False, f"No se encontró el archivo {nginx_conf}"

    required_headers = [
        "Strict-Transport-Security",
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Content-Security-Policy",
    ]

    with open(nginx_conf, "r", encoding="utf-8") as f:
        content = f.read()

    missing_headers = []
    for header in required_headers:
        if not re.search(rf"add_header\s+{header}", content):
            missing_headers.append(header)

    if missing_headers:
        return (
            False,
            f"Faltan los siguientes encabezados de seguridad: {', '.join(missing_headers)}",
        )

    return True, ""


def check_csrf_protection() -> Tuple[bool, str]:
    """Verifica la protección CSRF en el frontend y backend."""
    frontend_api = "frontend-call-automation/src/lib/api.js"

    if not os.path.isfile(frontend_api):
        return False, f"No se encontró el archivo {frontend_api}"

    with open(frontend_api, "r", encoding="utf-8") as f:
        content = f.read()

    if not re.search(r"csrf|xsrf", content, re.IGNORECASE):
        return False, "No se encontró protección CSRF en el cliente API del frontend"

    return True, ""


def check_security_md() -> Tuple[bool, str]:
    """Verifica el archivo SECURITY.md."""
    if not os.path.isfile("SECURITY.md"):
        return False, "No se encontró el archivo SECURITY.md"

    with open("SECURITY.md", "r", encoding="utf-8") as f:
        content = f.read()

    if not re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", content):
        return (
            False,
            "No se encontró una dirección de correo electrónico válida en SECURITY.md",
        )

    return True, ""


def mask_secret(secret: str) -> str:
    """
    Enmascara un secreto para evitar mostrarlo en texto claro.

    Args:
        secret: El secreto a enmascarar

    Returns:
        El secreto enmascarado, mostrando solo los primeros 4 caracteres
    """
    if not secret or len(secret) < 8:
        return "[SECRETO REDACTADO]"

    # Extraer solo la parte del valor después del signo igual
    if "=" in secret:
        parts = secret.split("=", 1)
        if len(parts) == 2:
            key, value = parts
            # Limpiar comillas
            value = value.strip()
            if value.startswith(("'", '"')) and value.endswith(("'", '"')):
                value = value[1:-1]
            # Enmascarar solo el valor
            if len(value) > 8:
                masked_value = value[:4] + "*" * (len(value) - 4)
            else:
                masked_value = "****"
            return f"{key}= [VALOR SENSIBLE: {masked_value}]"

    # Si no se puede separar, enmascarar todo el string
    visible_part = secret[:4]
    return f"{visible_part}{'*' * (len(secret) - 4)}"


def check_secrets_in_code() -> Tuple[bool, List[str]]:
    """Busca posibles secretos en el código."""
    patterns = [
        r'password\s*=\s*[\'"][^\'"]+[\'"]',
        r'api[_-]?key\s*=\s*[\'"][^\'"]+[\'"]',
        r'secret\s*=\s*[\'"][^\'"]+[\'"]',
        r'token\s*=\s*[\'"][^\'"]+[\'"]',
    ]

    exclude_dirs = [
        ".git",
        "node_modules",
        "venv",
        "__pycache__",
        ".next",
        "build",
        "dist",
    ]
    exclude_files = [".env.example", "security_check.py"]

    found_secrets = []

    for root, dirs, files in os.walk("."):
        # Excluir directorios
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            if file in exclude_files or file.endswith(
                (".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".woff", ".ttf")
            ):
                continue

            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                    for pattern in patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            # Ignorar valores de ejemplo o prueba
                            value = match.group(0)
                            if (
                                "example" in value.lower()
                                or "test" in value.lower()
                                or "dummy" in value.lower()
                            ):
                                continue
                            # Enmascarar el secreto antes de agregarlo a la lista
                            found_secrets.append(f"{file_path}: {mask_secret(value)}")
            except (UnicodeDecodeError, IsADirectoryError):
                continue

    return len(found_secrets) == 0, found_secrets


def main() -> int:
    """Función principal que ejecuta todas las verificaciones."""
    print_header("Verificación de Seguridad de CALLi")

    checks = [
        ("Archivo SECURITY.md", check_security_md()),
        ("Encabezados de Seguridad", check_security_headers()),
        ("Protección CSRF", check_csrf_protection()),
        ("Archivos .env", check_env_files()),
    ]

    all_passed = True
    for name, (status, message) in checks:
        print_result(name, status, message)
        if not status:
            all_passed = False

    print_header("Búsqueda de Secretos en el Código")
    secrets_check, found_secrets = check_secrets_in_code()
    print_result(
        "No hay secretos en el código",
        secrets_check,
        f"Se encontraron {len(found_secrets)} posibles secretos"
        if not secrets_check
        else "",
    )

    if not secrets_check:
        print(f"\n{Colors.YELLOW}Posibles secretos encontrados:{Colors.ENDC}")
        for secret in found_secrets[:10]:  # Mostrar solo los primeros 10
            # Los secretos ya están enmascarados por la función mask_secret
            print(f"  - {secret}")
        if len(found_secrets) > 10:
            print(f"  ... y {len(found_secrets) - 10} más")

    if all_passed and secrets_check:
        print(
            f"\n{Colors.GREEN}{Colors.BOLD}✓ Todas las verificaciones de seguridad pasaron{Colors.ENDC}"
        )
        return 0
    else:
        print(
            f"\n{Colors.RED}{Colors.BOLD}✗ Algunas verificaciones de seguridad fallaron{Colors.ENDC}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
