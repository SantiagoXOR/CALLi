#!/usr/bin/env python3
"""
Script para verificar las licencias de las dependencias.
Este script verifica que todas las dependencias tengan licencias compatibles.
"""

import json
import subprocess
import sys
from pathlib import Path

# Licencias compatibles con MIT
COMPATIBLE_LICENSES = [
    "MIT",
    "BSD",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "Apache",
    "Apache-2.0",
    "ISC",
    "CC0-1.0",
    "0BSD",
    "Unlicense",
    "WTFPL",
    "Python-2.0",
    "PSF-2.0",
    "MPL-2.0",
    "Zlib",
]

# Licencias que requieren revisión
REVIEW_LICENSES = [
    "LGPL",
    "LGPL-2.1",
    "LGPL-3.0",
    "MPL-1.1",
    "EPL-1.0",
    "EPL-2.0",
    "CDDL",
    "CPL",
]

# Licencias incompatibles
INCOMPATIBLE_LICENSES = [
    "GPL",
    "GPL-2.0",
    "GPL-3.0",
    "AGPL",
    "AGPL-3.0",
    "SSPL",
    "EUPL",
    "CC-BY-NC",
    "CC-BY-ND",
    "CC-BY-NC-SA",
    "CC-BY-NC-ND",
]


def check_python_licenses():
    """Verifica las licencias de las dependencias de Python."""
    print("Verificando licencias de dependencias de Python...")

    # Instalar pip-licenses si no está instalado
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "show", "pip-licenses"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except:
        print("Instalando pip-licenses...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pip-licenses"], check=False)

    # Obtener licencias
    result = subprocess.run(
        [sys.executable, "-m", "pip_licenses", "--format=json", "--with-system"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        print(f"Error al obtener licencias: {result.stderr}")
        return False

    try:
        licenses = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Error al parsear la salida de pip-licenses: {result.stdout}")
        return False

    incompatible = []
    review = []

    for pkg in licenses:
        pkg_name = pkg.get("Name", "")
        pkg_license = pkg.get("License", "").strip()

        if not pkg_license:
            review.append((pkg_name, "Desconocida"))
            continue

        # Verificar si la licencia es incompatible
        for incompatible_license in INCOMPATIBLE_LICENSES:
            if incompatible_license.lower() in pkg_license.lower():
                incompatible.append((pkg_name, pkg_license))
                break
        else:
            # Verificar si la licencia requiere revisión
            for review_license in REVIEW_LICENSES:
                if review_license.lower() in pkg_license.lower():
                    review.append((pkg_name, pkg_license))
                    break

    if incompatible:
        print("\n⚠️ Dependencias con licencias incompatibles:")
        for pkg_name, pkg_license in incompatible:
            print(f"  - {pkg_name}: {pkg_license}")

    if review:
        print("\n⚠️ Dependencias con licencias que requieren revisión:")
        for pkg_name, pkg_license in review:
            print(f"  - {pkg_name}: {pkg_license}")

    if not incompatible and not review:
        print("✅ Todas las dependencias de Python tienen licencias compatibles")
        return True

    return False


def check_js_licenses():
    """Verifica las licencias de las dependencias de JavaScript."""
    print("Verificando licencias de dependencias de JavaScript...")

    frontend_dir = Path("frontend-call-automation")
    if not frontend_dir.exists() or not (frontend_dir / "package.json").exists():
        print("⚠️ No se encontró el directorio de frontend o el archivo package.json")
        return True

    # Instalar license-checker si no está instalado
    try:
        result = subprocess.run(
            ["npx", "license-checker", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            print("Instalando license-checker...")
            subprocess.run(["npm", "install", "-g", "license-checker"], check=False)
    except:
        print("Error al verificar license-checker. Asegúrate de tener Node.js instalado.")
        return False

    # Obtener licencias
    result = subprocess.run(
        ["npx", "license-checker", "--json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=frontend_dir,
        check=False,
    )

    if result.returncode != 0:
        print(f"Error al obtener licencias: {result.stderr}")
        return False

    try:
        licenses = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Error al parsear la salida de license-checker: {result.stdout}")
        return False

    incompatible = []
    review = []

    for pkg_path, pkg_info in licenses.items():
        pkg_name = pkg_path.split("@")[0]
        pkg_license = pkg_info.get("licenses", "").strip()

        if not pkg_license:
            review.append((pkg_name, "Desconocida"))
            continue

        # Verificar si la licencia es incompatible
        for incompatible_license in INCOMPATIBLE_LICENSES:
            if incompatible_license.lower() in pkg_license.lower():
                incompatible.append((pkg_name, pkg_license))
                break
        else:
            # Verificar si la licencia requiere revisión
            for review_license in REVIEW_LICENSES:
                if review_license.lower() in pkg_license.lower():
                    review.append((pkg_name, pkg_license))
                    break

    if incompatible:
        print("\n⚠️ Dependencias con licencias incompatibles:")
        for pkg_name, pkg_license in incompatible:
            print(f"  - {pkg_name}: {pkg_license}")

    if review:
        print("\n⚠️ Dependencias con licencias que requieren revisión:")
        for pkg_name, pkg_license in review:
            print(f"  - {pkg_name}: {pkg_license}")

    if not incompatible and not review:
        print("✅ Todas las dependencias de JavaScript tienen licencias compatibles")
        return True

    return False


def create_license_exceptions_file():
    """Crea un archivo de excepciones de licencias."""
    exceptions_file = Path("license-exceptions.json")
    if not exceptions_file.exists():
        exceptions = {
            "exceptions": [
                {
                    "package": "example-package",
                    "version": "1.0.0",
                    "license": "GPL-3.0",
                    "reason": "Este paquete solo se usa en desarrollo, no en producción",
                    "approved_by": "Equipo Legal",
                    "approved_date": "2025-01-01",
                }
            ]
        }

        with open(exceptions_file, "w", encoding="utf-8") as f:
            json.dump(exceptions, f, indent=2)

        print(f"✅ Archivo {exceptions_file} creado")
    else:
        print(f"✅ Archivo {exceptions_file} verificado")


def main():
    """Función principal."""
    print("🔍 Verificando licencias de dependencias...")

    # Verificar licencias de Python
    python_ok = check_python_licenses()

    # Verificar licencias de JavaScript
    js_ok = check_js_licenses()

    # Crear archivo de excepciones
    create_license_exceptions_file()

    if python_ok and js_ok:
        print("\n✅ Todas las dependencias tienen licencias compatibles")
        return 0
    print("\n⚠️ Se encontraron problemas con las licencias de algunas dependencias")
    print("   Revisa las dependencias mencionadas y considera:")
    print("   1. Reemplazarlas por alternativas con licencias compatibles")
    print("   2. Documentar excepciones en el archivo license-exceptions.json")
    return 1


if __name__ == "__main__":
    sys.exit(main())
