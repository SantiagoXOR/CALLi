#!/usr/bin/env python3
"""
Script para verificar la seguridad del backend.
Este script realiza verificaciones de seguridad en el código del backend.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


def run_bandit():
    """Ejecuta Bandit para analizar el código Python."""
    print("Ejecutando Bandit para analizar el código Python...")

    # Instalar bandit si no está instalado
    try:
        subprocess.run(
            ["bandit", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
        )
    except:
        print("Instalando bandit...")
        subprocess.run([sys.executable, "-m", "pip", "install", "bandit"], check=False)

    # Crear directorio para informes
    os.makedirs("security-reports", exist_ok=True)

    # Ejecutar bandit
    result = subprocess.run(
        [
            "bandit",
            "-r",
            "backend-call-automation",
            "-f",
            "json",
            "-o",
            "security-reports/bandit-results.json",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    if (
        result.returncode != 0 and result.returncode != 1
    ):  # 1 significa que se encontraron problemas
        print(f"Error al ejecutar bandit: {result.stderr}")
        return False

    # Verificar resultados
    try:
        if os.path.exists("security-reports/bandit-results.json"):
            with open("security-reports/bandit-results.json") as f:
                results = json.load(f)

            high_severity = 0
            medium_severity = 0

            for result in results.get("results", []):
                severity = result.get("issue_severity", "")
                if severity == "HIGH":
                    high_severity += 1
                elif severity == "MEDIUM":
                    medium_severity += 1

            if high_severity > 0:
                print(f"⚠️ Se encontraron {high_severity} problemas de alta severidad")
                return False

            if medium_severity > 0:
                print(f"⚠️ Se encontraron {medium_severity} problemas de severidad media")

            print("✅ Análisis de Bandit completado")
            return True
        print("⚠️ No se generó el archivo de resultados de Bandit")
        return False
    except Exception as e:
        print(f"Error al procesar los resultados de Bandit: {e!s}")
        return False


def run_safety():
    """Ejecuta Safety para verificar vulnerabilidades en dependencias."""
    print("Ejecutando Safety para verificar vulnerabilidades en dependencias...")

    # Instalar safety si no está instalado
    try:
        subprocess.run(
            ["safety", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
        )
    except:
        print("Instalando safety...")
        subprocess.run([sys.executable, "-m", "pip", "install", "safety"], check=False)

    # Verificar si existe requirements.txt
    requirements_file = Path("backend-call-automation/requirements.txt")
    if not requirements_file.exists():
        print(f"⚠️ No se encontró el archivo {requirements_file}")
        return True

    # Ejecutar safety
    result = subprocess.run(
        ["safety", "check", "-r", str(requirements_file), "--json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    # Guardar resultados
    os.makedirs("security-reports", exist_ok=True)
    with open("security-reports/safety-results.json", "w") as f:
        f.write(result.stdout)

    if result.returncode != 0:
        try:
            vulnerabilities = json.loads(result.stdout)
            if isinstance(vulnerabilities, list) and len(vulnerabilities) > 0:
                print(f"⚠️ Se encontraron {len(vulnerabilities)} vulnerabilidades en dependencias")
                return False
        except:
            print(f"⚠️ Error al analizar los resultados de Safety: {result.stderr}")
            return False

    print("✅ Análisis de Safety completado")
    return True


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


def check_hardcoded_secrets():
    """Busca secretos hardcodeados en el código."""
    print("Buscando secretos hardcodeados en el código...")

    # Patrones para buscar secretos
    patterns = [
        r'password\s*=\s*[\'"][^\'"]+[\'"]',
        r'api[_-]?key\s*=\s*[\'"][^\'"]+[\'"]',
        r'secret\s*=\s*[\'"][^\'"]+[\'"]',
        r'token\s*=\s*[\'"][^\'"]+[\'"]',
    ]

    # Directorios a excluir
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
    ]

    # Archivos a excluir
    exclude_files = [
        ".env.example",
        "security_check.py",
        "security_check_local.py",
        "backend_security_check.py",
        "docker-compose.yml",
        "docker-compose.prod.yml",
        "docker-compose.monitoring.yml",
    ]

    # Buscar en el directorio del backend
    backend_dir = Path("backend-call-automation")
    if not backend_dir.exists():
        print(f"⚠️ No se encontró el directorio {backend_dir}")
        return True

    found_secrets = []

    for root, dirs, files in os.walk(backend_dir):
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
                            # Enmascarar el secreto antes de agregarlo a la lista
                            found_secrets.append(f"{file_path}: {mask_secret(value)}")
            except (UnicodeDecodeError, IsADirectoryError, PermissionError):
                continue

    if found_secrets:
        print(f"⚠️ Se encontraron {len(found_secrets)} posibles secretos hardcodeados:")
        for secret in found_secrets[:5]:  # Mostrar solo los primeros 5 para no exponer todos
            # Los secretos ya están enmascarados por la función mask_secret
            print(f"  - {secret}")

        if len(found_secrets) > 5:
            print(f"  ... y {len(found_secrets) - 5} más")

        return False

    print("✅ No se encontraron secretos hardcodeados")
    return True


def check_security_headers():
    """Verifica los encabezados de seguridad en la configuración de nginx."""
    print("Verificando encabezados de seguridad...")

    nginx_conf = Path("nginx/conf.d/default.conf")
    if not nginx_conf.exists():
        print(f"⚠️ No se encontró el archivo {nginx_conf}")
        return True

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
        print(f"⚠️ Faltan los siguientes encabezados de seguridad: {', '.join(missing_headers)}")
        return False

    print("✅ Todos los encabezados de seguridad requeridos están presentes")
    return True


def main():
    """Función principal."""
    print("🔒 Verificando seguridad del backend...")

    # Ejecutar verificaciones
    bandit_ok = run_bandit()
    safety_ok = run_safety()
    secrets_ok = check_hardcoded_secrets()
    headers_ok = check_security_headers()

    # Verificar resultados
    if bandit_ok and safety_ok and secrets_ok and headers_ok:
        print("\n✅ Todas las verificaciones de seguridad pasaron")
        return 0
    print("\n⚠️ Algunas verificaciones de seguridad fallaron")
    if not bandit_ok:
        print("  - Bandit encontró problemas de seguridad en el código")
    if not safety_ok:
        print("  - Safety encontró vulnerabilidades en dependencias")
    if not secrets_ok:
        print("  - Se encontraron secretos hardcodeados en el código")
    if not headers_ok:
        print("  - Faltan encabezados de seguridad en la configuración de nginx")

    print("\nPor favor, corrige estos problemas antes de continuar.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
