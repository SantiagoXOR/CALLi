#!/usr/bin/env python3
"""
Utilidades mejoradas para la seguridad del proyecto CALLi.
Este módulo contiene funciones para mejorar la seguridad del proyecto.
"""

import hashlib
import os
import random
import re
import string


def secure_mask_secret(secret: str, show_prefix: bool = False) -> str:
    """
    Enmascara un secreto de manera segura para evitar mostrarlo en texto claro.
    Esta versión mejorada no muestra ninguna parte del secreto original.

    Args:
        secret: El secreto a enmascarar
        show_prefix: Si es True, muestra un hash del prefijo para ayudar a identificar
                    el secreto sin revelar su contenido

    Returns:
        El secreto enmascarado de forma segura
    """
    if not secret:
        return "[SECRETO VACÍO]"

    # Extraer solo la parte del valor después del signo igual
    key = None
    value = secret
    if "=" in secret:
        parts = secret.split("=", 1)
        if len(parts) == 2:
            key, value = parts
            # Limpiar comillas
            value = value.strip()
            if value.startswith(("'", '"')) and value.endswith(("'", '"')):
                value = value[1:-1]

    # Generar un hash del secreto para referencia (solo para fines de identificación)
    # Esto no revela el contenido pero permite identificar secretos duplicados
    hash_id = hashlib.sha256(value.encode()).hexdigest()[:8]

    # Determinar la longitud aproximada para dar una idea del tamaño sin revelar el contenido exacto
    length_category = "corto" if len(value) < 16 else "medio" if len(value) < 32 else "largo"

    if key:
        if show_prefix and len(value) > 4:
            # Crear un hash del prefijo en lugar de mostrar los caracteres reales
            prefix_hash = hashlib.md5(value[:4].encode()).hexdigest()[:6]
            return f"{key}= [VALOR SENSIBLE: longitud={length_category}, id={hash_id}, prefijo-hash={prefix_hash}]"
        return f"{key}= [VALOR SENSIBLE: longitud={length_category}, id={hash_id}]"

    # Si no hay clave, solo devolver información sobre el secreto
    return f"[SECRETO: longitud={length_category}, id={hash_id}]"


def find_secrets(
    base_dirs: list[str] = None,
    exclude_dirs: list[str] = None,
    exclude_files: list[str] = None,
    additional_patterns: list[str] = None,
) -> tuple[bool, list[str]]:
    """
    Busca posibles secretos en el código de manera más exhaustiva.

    Args:
        base_dirs: Directorios base donde buscar (si es None, usa directorios predeterminados)
        exclude_dirs: Directorios a excluir (si es None, usa exclusiones predeterminadas)
        exclude_files: Archivos a excluir (si es None, usa exclusiones predeterminadas)
        additional_patterns: Patrones adicionales para buscar secretos

    Returns:
        Tupla con un booleano (True si no hay secretos) y una lista de secretos encontrados
    """
    # Patrones predeterminados para buscar secretos
    patterns = [
        r'password\s*=\s*[\'"][^\'"]+[\'"]',
        r'passwd\s*=\s*[\'"][^\'"]+[\'"]',
        r'api[_-]?key\s*=\s*[\'"][^\'"]+[\'"]',
        r'secret\s*=\s*[\'"][^\'"]+[\'"]',
        r'token\s*=\s*[\'"][^\'"]+[\'"]',
        r'auth[_-]?token\s*=\s*[\'"][^\'"]+[\'"]',
        r'credentials\s*=\s*[\'"][^\'"]+[\'"]',
        r'private[_-]?key\s*=\s*[\'"][^\'"]+[\'"]',
        # Patrones para detectar URLs con credenciales
        r'https?://[^:]+:[^@]+@[^\'"]+',
        # Patrones para detectar variables de entorno con valores sensibles
        r'os\.environ\[[\'"](?:API_KEY|SECRET|TOKEN|PASSWORD|CREDENTIAL)[\'"]]\s*=\s*[\'"][^\'"]+[\'"]',
        r'env\.[\'"](?:API_KEY|SECRET|TOKEN|PASSWORD|CREDENTIAL)[\'"]]\s*=\s*[\'"][^\'"]+[\'"]',
    ]

    # Agregar patrones adicionales si se proporcionan
    if additional_patterns:
        patterns.extend(additional_patterns)

    # Directorios predeterminados a excluir
    default_exclude_dirs = [
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
        "coverage",
        ".coverage",
        ".idea",
        ".vscode",
    ]

    # Usar exclusiones proporcionadas o predeterminadas
    exclude_dirs = exclude_dirs or default_exclude_dirs

    # Archivos predeterminados a excluir
    default_exclude_files = [
        ".env.example",
        "security_check.py",
        "security_check_local.py",
        "backend_security_check.py",
        "improved_security_utils.py",
        "docker-compose.yml",
        "docker-compose.prod.yml",
        "docker-compose.monitoring.yml",
        "package-lock.json",
        "yarn.lock",
    ]

    # Usar exclusiones de archivos proporcionadas o predeterminadas
    exclude_files = exclude_files or default_exclude_files

    # Directorios base predeterminados para buscar
    default_base_dirs = [
        "backend-call-automation",
        "frontend-call-automation",
        "scripts",
        "app",
        "src",
        "config",
        "nginx",
    ]

    # Usar directorios base proporcionados o predeterminados
    base_dirs = base_dirs or default_base_dirs

    found_secrets = []

    # Filtrar solo los directorios base que existen
    existing_base_dirs = [d for d in base_dirs if os.path.exists(d)]

    for base_dir in existing_base_dirs:
        for root, dirs, files in os.walk(base_dir):
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
                        ".eot",
                        ".mp3",
                        ".mp4",
                        ".avi",
                        ".mov",
                        ".webm",
                        ".pdf",
                        ".zip",
                        ".tar",
                        ".gz",
                        ".rar",
                        ".7z",
                        ".exe",
                        ".dll",
                        ".so",
                        ".dylib",
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
                                    or "sample" in value.lower()
                                    or "placeholder" in value.lower()
                                ):
                                    continue

                                # Obtener el número de línea
                                line_number = content[: match.start()].count("\n") + 1

                                # Almacenar la ubicación del secreto pero enmascarar el valor de forma segura
                                found_secrets.append(
                                    f"{file_path}:{line_number}: {secure_mask_secret(value)}"
                                )
                except (UnicodeDecodeError, IsADirectoryError, PermissionError):
                    continue

    return len(found_secrets) == 0, found_secrets


def generate_secure_random_string(length: int = 32) -> str:
    """
    Genera una cadena aleatoria segura para usar como secreto.

    Args:
        length: Longitud de la cadena a generar

    Returns:
        Una cadena aleatoria segura
    """
    # Usar caracteres seguros para evitar problemas de codificación
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
    # Usar random.SystemRandom() para obtener entropía del sistema operativo
    secure_random = random.SystemRandom()
    return "".join(secure_random.choice(chars) for _ in range(length))


if __name__ == "__main__":
    # Ejemplo de uso
    print("Utilidades de seguridad mejoradas para CALLi")
    print("Ejecute este módulo desde otro script para usar sus funciones.")

    # Demostración de enmascaramiento seguro
    test_secret = "api_key='abcd1234efgh5678'"
    print(f"Original: {test_secret}")
    print(f"Enmascarado (inseguro): {test_secret[:7]}{'*' * (len(test_secret) - 7)}")
    print(f"Enmascarado (seguro): {secure_mask_secret(test_secret)}")

    # Generar un secreto aleatorio seguro
    print(f"Secreto aleatorio seguro: {generate_secure_random_string()}")
