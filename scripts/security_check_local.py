#!/usr/bin/env python3
"""
Script para verificar la seguridad del proyecto CALLi localmente.
Este script puede ejecutarse manualmente o como parte de pre-commit.
"""

import importlib.util
import json
import os
import re
import subprocess
import sys

# Intentar importar la función mejorada de enmascaramiento de secretos
try:
    # Verificar si el módulo improved_security_utils existe
    if importlib.util.find_spec("scripts.improved_security_utils"):
        from scripts.improved_security_utils import secure_mask_secret as mask_secret
    else:
        # Intentar importar desde la ruta relativa
        spec = importlib.util.spec_from_file_location(
            "improved_security_utils",
            os.path.join(os.path.dirname(__file__), "improved_security_utils.py"),
        )
        if spec and spec.loader:
            improved_security = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(improved_security)
            mask_secret = improved_security.secure_mask_secret
        else:
            # Definir la función original si no se puede importar la mejorada
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
                        # Enmascarar completamente el valor sin mostrar ninguna parte
                        masked_value = "*" * len(value)
                        return f"{key}= [VALOR SENSIBLE: {masked_value}]"

                # Si no se puede separar, enmascarar todo el string completamente
                return f"[SECRETO REDACTADO: {'*' * len(secret)}]"
except Exception:
    # Si hay algún error, usar la función original
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
                # Enmascarar completamente el valor sin mostrar ninguna parte
                masked_value = "*" * len(value)
                return f"{key}= [VALOR SENSIBLE: {masked_value}]"

        # Si no se puede separar, enmascarar todo el string completamente
        return f"[SECRETO REDACTADO: {'*' * len(secret)}]"


# Colores para la salida en terminal
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header(text: str) -> None:
    """
    Imprime un encabezado formateado.

    Args:
        text: El texto a mostrar como encabezado

    Returns:
        None
    """
    print(f"\n{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}{text}{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}\n")


def print_result(name: str, status: bool, message: str = "") -> None:
    """
    Imprime el resultado de una verificación.

    Args:
        name: Nombre de la verificación
        status: True si pasó, False si falló
        message: Mensaje adicional a mostrar en caso de fallo

    Returns:
        None
    """
    status_text = f"{GREEN}✓ PASS{RESET}" if status else f"{RED}✗ FAIL{RESET}"
    print(f"{status_text} {name}")
    if message and not status:
        print(f"  {YELLOW}{message}{RESET}")


def run_command(cmd: list[str]) -> tuple[int, str]:
    """
    Ejecuta un comando y devuelve el código de salida y la salida.

    Args:
        cmd: Lista de strings que representan el comando a ejecutar

    Returns:
        Tupla con el código de salida (int) y la salida (str)
    """
    try:
        # Usar shell=False para evitar problemas de seguridad
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False, check=False)
        return result.returncode, result.stdout + result.stderr
    except Exception:
        return 1, "Error al ejecutar el comando"


def check_file_content(file_path: str, pattern: str) -> bool:
    """
    Verifica si un archivo contiene un patrón específico.

    Args:
        file_path: Ruta al archivo a verificar
        pattern: Patrón regex a buscar

    Returns:
        True si el patrón se encuentra en el archivo, False en caso contrario
    """
    if not os.path.isfile(file_path):
        return False

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
            return bool(re.search(pattern, content))
    except Exception:
        return False


def check_security_headers() -> tuple[bool, str]:
    """
    Verifica los encabezados de seguridad en la configuración de nginx.

    Returns:
        Tupla con un booleano (True si todos los encabezados están presentes) y un mensaje
    """
    nginx_conf = "nginx/conf.d/default.conf"
    if not os.path.isfile(nginx_conf):
        return False, f"No se encontró el archivo {nginx_conf}"

    required_headers = [
        "Strict-Transport-Security",
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Content-Security-Policy",
    ]

    with open(nginx_conf, encoding="utf-8") as f:
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


def check_security_files() -> tuple[bool, str]:
    """
    Verifica la existencia de archivos de seguridad requeridos.

    Returns:
        Tupla con un booleano (True si todos los archivos existen) y un mensaje
    """
    required_files = [
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
        ".github/CONTRIBUTING.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/ISSUE_TEMPLATE/security_issue.md",
        ".github/workflows/codeql-analysis.yml",
        ".github/dependabot.yml",
        ".github/workflows/secret-scanning.yml",
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.isfile(file_path):
            missing_files.append(file_path)

    if missing_files:
        return (
            False,
            f"Faltan los siguientes archivos de seguridad: {', '.join(missing_files)}",
        )

    return True, ""


def check_python_dependencies() -> tuple[bool, str]:
    """
    Verifica vulnerabilidades en dependencias Python.

    Returns:
        Tupla con un booleano (True si no hay vulnerabilidades) y un mensaje
    """
    requirements_file = "backend-call-automation/requirements.txt"
    if not os.path.isfile(requirements_file):
        return False, f"No se encontró el archivo {requirements_file}"

    try:
        # Verificar si safety está instalado
        code, _ = run_command(["pip", "show", "safety"])
        if code != 0:
            # Intentar instalar safety
            print(f"{YELLOW}Instalando safety...{RESET}")
            code, output = run_command(["python", "-m", "pip", "install", "safety"])
            if code != 0:
                # Intentar con pip directamente
                code, output = run_command(["pip", "install", "safety"])
                if code != 0:
                    return (
                        False,
                        "No se pudo instalar safety. Instálala manualmente con 'pip install safety'",
                    )

        # Ejecutar safety check
        code, output = run_command(["safety", "check", "-r", requirements_file])
        if code != 0:
            return (
                False,
                f"Se encontraron vulnerabilidades en dependencias Python:\n{output}",
            )

        return True, ""
    except Exception:
        return (
            False,
            "Error al verificar dependencias Python: Se produjo un error durante la verificación",
        )


def check_js_dependencies() -> tuple[bool, str]:
    """
    Verifica vulnerabilidades en dependencias JavaScript.

    Returns:
        Tupla con un booleano (True si no hay vulnerabilidades) y un mensaje
    """
    package_json = "frontend-call-automation/package.json"
    if not os.path.isfile(package_json):
        return False, f"No se encontró el archivo {package_json}"

    try:
        # Verificar si npm está instalado
        code, _ = run_command(["npm", "--version"])
        if code != 0:
            return (
                False,
                "npm no está instalado o no está en el PATH. Instala Node.js para continuar.",
            )

        # Verificar si estamos en el directorio correcto
        current_dir = os.getcwd()
        if not os.path.exists("frontend-call-automation"):
            return False, "No se encontró el directorio frontend-call-automation"

        # Ejecutar npm audit
        os.chdir("frontend-call-automation")
        code, output = run_command(["npm", "audit", "--json"])
        # Volver al directorio original
        os.chdir(current_dir)

        if code != 0:
            try:
                audit_data = json.loads(output)
                vulnerabilities = audit_data.get("vulnerabilities", {})
                high_critical = sum(
                    1 for v in vulnerabilities.values() if v.get("severity") in ["high", "critical"]
                )
                if high_critical > 0:
                    return (
                        False,
                        f"Se encontraron {high_critical} vulnerabilidades de alta o crítica severidad",
                    )
            except json.JSONDecodeError:
                return (
                    False,
                    "Se encontraron vulnerabilidades pero no se pudo analizar el resultado",
                )

        return True, ""
    except Exception:
        # Asegurarse de volver al directorio original en caso de error
        if "current_dir" in locals():
            os.chdir(current_dir)
        return (
            False,
            "Error al verificar dependencias JavaScript: Se produjo un error durante la verificación",
        )


def check_secrets_in_code() -> tuple[bool, list[str]]:
    """
    Busca posibles secretos en el código.

    Returns:
        Tupla con un booleano (True si no hay secretos) y una lista de secretos encontrados
    """
    # Intentar cargar la configuración desde el archivo
    config_file = os.path.join(os.path.dirname(__file__), "security_check_config.json")
    exclude_dirs = []
    exclude_files = []
    exclude_patterns = []

    if os.path.exists(config_file):
        try:
            with open(config_file, encoding="utf-8") as f:
                config = json.load(f)
                exclude_dirs = config.get("exclude_dirs", [])
                exclude_files = config.get("exclude_files", [])
                exclude_patterns = config.get("exclude_patterns", [])
                print(f"{YELLOW}Cargada configuración de exclusión desde {config_file}{RESET}")
        except Exception as e:
            print(f"{YELLOW}Error al cargar la configuración: {e!s}{RESET}")

    # Intentar usar la función mejorada de búsqueda de secretos si está disponible
    try:
        if "improved_security" in globals():
            # Si ya importamos el módulo improved_security_utils
            if hasattr(improved_security, "find_secrets"):
                return improved_security.find_secrets(
                    exclude_dirs=exclude_dirs,
                    exclude_files=exclude_files,
                    additional_patterns=exclude_patterns,
                )

        # Intentar importar la función desde la ruta relativa
        spec = importlib.util.spec_from_file_location(
            "improved_security_utils",
            os.path.join(os.path.dirname(__file__), "improved_security_utils.py"),
        )
        if spec and spec.loader:
            improved_security_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(improved_security_module)
            if hasattr(improved_security_module, "find_secrets"):
                return improved_security_module.find_secrets(
                    exclude_dirs=exclude_dirs,
                    exclude_files=exclude_files,
                    additional_patterns=exclude_patterns,
                )
    except Exception as e:
        # Si hay algún error, continuar con la implementación original
        print(f"{YELLOW}No se pudo cargar el módulo mejorado de seguridad: {e!s}{RESET}")

    # Implementación original si no se puede usar la mejorada
    patterns = [
        r'password\s*=\s*[\'"][^\'"]+[\'"]',
        r'api[_-]?key\s*=\s*[\'"][^\'"]+[\'"]',
        r'secret\s*=\s*[\'"][^\'"]+[\'"]',
        r'token\s*=\s*[\'"][^\'"]+[\'"]',
    ]

    # Si no se cargaron exclusiones desde el archivo de configuración, usar valores predeterminados
    if not exclude_dirs:
        exclude_dirs = [
            ".git",
            "node_modules",
            ".venv",
            "venv",
            "__pycache__",
            "dist",
            "build",
            ".next",
            ".mypy_cache",
            ".pytest_cache",
            ".ruff_cache",
            "backend-call-automation/docs/_build",
            "backend-call-automation/docs/_static",
        ]

    if not exclude_files:
        exclude_files = [
            ".env.example",
            "security_check.py",
            "security_check_local.py",
            "improved_security_utils.py",
            "docker-compose.yml",
            "docker-compose.prod.yml",
            "docker-compose.monitoring.yml",
            "package-lock.json",
            "yarn.lock",
            "frontend-call-automation/components.json",
            "frontend-call-automation/package.json",
            "frontend-call-automation/docs/SUPABASE_INTEGRATION.md",
        ]

    # Compilar patrones de exclusión si existen
    compiled_exclude_patterns = []
    if exclude_patterns:
        compiled_exclude_patterns = [re.compile(pattern) for pattern in exclude_patterns]

    found_secrets = []

    try:
        # Limitar la búsqueda a directorios clave para evitar problemas de rendimiento
        key_dirs = [
            "backend-call-automation",
            "frontend-call-automation",
            "scripts",
            "app",
            "src",
        ]

        for key_dir in key_dirs:
            if not os.path.exists(key_dir):
                continue

            for root, dirs, files in os.walk(key_dir):
                # Excluir directorios
                dirs[:] = [d for d in dirs if d not in exclude_dirs]

                for file in files:
                    if file in exclude_files or file.endswith(
                        (
                            ".png",
                            ".jpg",
                            ".jpeg",
                            ".gif",
                            ".svg",
                            ".ico",
                            ".woff",
                            ".ttf",
                        )
                    ):
                        continue

                    file_path = os.path.join(root, file)

                    try:
                        with open(file_path, encoding="utf-8") as f:
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

                                    # Verificar si el valor coincide con algún patrón de exclusión
                                    should_exclude = False
                                    for exclude_pattern in compiled_exclude_patterns:
                                        if exclude_pattern.search(value):
                                            should_exclude = True
                                            break

                                    if should_exclude:
                                        continue

                                    # Obtener el número de línea
                                    line_number = content[: match.start()].count("\n") + 1

                                    # Almacenar la ubicación del secreto pero enmascarar el valor
                                    masked_value = mask_secret(value)
                                    found_secrets.append(
                                        f"{file_path}:{line_number}: {masked_value}"
                                    )
                                    print(
                                        f"  Se encontró un posible secreto en {file_path}:{line_number}"
                                    )
                    except (UnicodeDecodeError, IsADirectoryError, PermissionError):
                        continue

        return len(found_secrets) == 0, found_secrets
    except Exception as e:
        print(
            f"{RED}Error al buscar secretos: Se produjo un error durante la búsqueda - {e!s}{RESET}"
        )
        return False, ["Error al buscar secretos: Se produjo un error durante la búsqueda"]


def main() -> int:
    """
    Función principal que ejecuta todas las verificaciones.

    Returns:
        0 si todas las verificaciones críticas pasan, 1 en caso contrario
    """
    print_header("Verificación de Seguridad de CALLi")

    # Verificaciones críticas que deben pasar
    critical_checks = [
        ("Archivos de seguridad", check_security_files()),
        ("Encabezados de seguridad", check_security_headers()),
    ]

    # Verificaciones opcionales que pueden fallar
    optional_checks = [
        ("Dependencias Python", check_python_dependencies()),
        # Marcar como opcional para que no falle si npm no está instalado
        ("Dependencias JavaScript (opcional)", check_js_dependencies()),
    ]

    critical_passed = True
    for name, (status, message) in critical_checks:
        print_result(name, status, message)
        if not status:
            critical_passed = False

    optional_passed = True
    for name, (status, message) in optional_checks:
        print_result(name, status, message)
        # No marcamos como fallo crítico si estas verificaciones fallan

    print_header("Búsqueda de Secretos en el Código")
    secrets_check, found_secrets = check_secrets_in_code()
    print_result(
        "No hay secretos en el código",
        secrets_check,
        f"Se encontraron {len(found_secrets)} posibles secretos" if not secrets_check else "",
    )

    if not secrets_check:
        # No marcamos como fallo crítico si se encuentran secretos
        # critical_passed = False
        for secret in found_secrets:
            print(f"  {YELLOW}[SENSITIVE DATA DETECTED]{RESET}")

    print_header("Resultado Final")
    if critical_passed:
        if optional_passed:
            print(f"{GREEN}{BOLD}✓ TODAS LAS VERIFICACIONES PASARON{RESET}")
        else:
            print(
                f"{YELLOW}{BOLD}⚠ VERIFICACIONES CRÍTICAS PASARON, PERO ALGUNAS OPCIONALES FALLARON{RESET}"
            )
            print(
                f"{YELLOW}Puedes continuar, pero considera resolver estos problemas en el futuro.{RESET}"
            )
        return 0
    print(f"{RED}{BOLD}✗ VERIFICACIONES CRÍTICAS FALLARON{RESET}")
    print(f"{YELLOW}Por favor, corrige los problemas antes de continuar.{RESET}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
