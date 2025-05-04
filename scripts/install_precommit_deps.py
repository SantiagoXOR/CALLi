#!/usr/bin/env python3
"""
Script para instalar todas las dependencias necesarias para pre-commit.
"""

import platform
import subprocess
import sys

# Colores para la salida en terminal
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header(text: str) -> None:
    """Imprime un encabezado formateado."""
    print(f"\n{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}{text}{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}\n")


def run_command(cmd: list[str], cwd: str | None = None) -> tuple[int, str]:
    """
    Ejecuta un comando y devuelve el código de salida y la salida.

    Args:
        cmd: Lista de strings que representan el comando a ejecutar
        cwd: Directorio de trabajo para ejecutar el comando

    Returns:
        Tupla con el código de salida (int) y la salida (str)
    """
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, check=False)
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error al ejecutar el comando: {e!s}"


def install_python_deps() -> bool:
    """Instala las dependencias de Python necesarias para pre-commit."""
    print_header("Instalando dependencias de Python")

    python_deps = [
        "pre-commit",
        "bandit[toml]",
        "safety",
        "mypy",
        "types-requests",
        "types-PyYAML",
        "types-python-dateutil",
        "types-setuptools",
        "types-toml",
        "types-redis",
        "types-urllib3",
        "docutils",
        "restructuredtext-lint",  # Nombre correcto del paquete rst-lint
        "ruff",
    ]

    print(f"Instalando: {', '.join(python_deps)}")
    code, output = run_command([sys.executable, "-m", "pip", "install", "--upgrade"] + python_deps)

    if code != 0:
        print(f"{RED}Error al instalar dependencias de Python:{RESET}\n{output}")
        return False

    print(f"{GREEN}Dependencias de Python instaladas correctamente.{RESET}")
    return True


def install_gitleaks() -> bool:
    """Instala Gitleaks según el sistema operativo."""
    print_header("Instalando Gitleaks")

    system = platform.system().lower()

    if system == "windows":
        print("En Windows, se recomienda instalar Gitleaks usando Chocolatey:")
        print("  choco install gitleaks")
        print("O descargar el binario desde: https://github.com/gitleaks/gitleaks/releases")
        return True
    if system == "darwin":  # macOS
        code, output = run_command(["brew", "install", "gitleaks"])
        if code != 0:
            print(
                f"{YELLOW}No se pudo instalar Gitleaks con Homebrew. Intente instalarlo manualmente:{RESET}"
            )
            print("  Descargue desde: https://github.com/gitleaks/gitleaks/releases")
            return False
    elif system == "linux":
        # Intentar con apt-get para distribuciones basadas en Debian
        code, output = run_command(["apt-get", "install", "-y", "gitleaks"])
        if code != 0:
            # Intentar con snap
            code, output = run_command(["snap", "install", "gitleaks"])
            if code != 0:
                print(
                    f"{YELLOW}No se pudo instalar Gitleaks automáticamente. Intente instalarlo manualmente:{RESET}"
                )
                print("  Descargue desde: https://github.com/gitleaks/gitleaks/releases")
                return False

    # Verificar la instalación
    code, output = run_command(["gitleaks", "version"])
    if code != 0:
        print(f"{RED}Gitleaks no se instaló correctamente.{RESET}")
        return False

    print(f"{GREEN}Gitleaks instalado correctamente: {output.strip()}{RESET}")
    return True


def install_kics() -> bool:
    """Instala KICS según el sistema operativo."""
    print_header("Instalando KICS")

    system = platform.system().lower()

    if system == "windows":
        print("En Windows, descargue KICS desde: https://github.com/Checkmarx/kics/releases")
        print("Y agregue el directorio bin a su PATH.")
        return True
    # Usar el script de instalación oficial para Linux/macOS
    print("Instalando KICS usando el script oficial...")
    code, output = run_command(
        [
            "curl",
            "-sfL",
            "https://raw.githubusercontent.com/Checkmarx/kics/master/install.sh",
            "|",
            "sh",
        ]
    )

    if code != 0:
        print(f"{RED}Error al instalar KICS:{RESET}\n{output}")
        print("Descargue manualmente desde: https://github.com/Checkmarx/kics/releases")
        return False

    # Verificar la instalación
    code, output = run_command(["kics", "version"])
    if code != 0:
        print(f"{RED}KICS no se instaló correctamente.{RESET}")
        return False

    print(f"{GREEN}KICS instalado correctamente.{RESET}")
    return True


def install_pre_commit_hooks() -> bool:
    """Instala los hooks de pre-commit."""
    print_header("Instalando hooks de pre-commit")

    code, output = run_command(["pre-commit", "install"])
    if code != 0:
        print(f"{RED}Error al instalar hooks de pre-commit:{RESET}\n{output}")
        return False

    print(f"{GREEN}Hooks de pre-commit instalados correctamente.{RESET}")
    return True


def main() -> int:
    """Función principal."""
    print_header("Instalación de dependencias para pre-commit")

    # Instalar dependencias de Python
    if not install_python_deps():
        print(f"{RED}No se pudieron instalar todas las dependencias de Python.{RESET}")
        return 1

    # Instalar Gitleaks
    if not install_gitleaks():
        print(
            f"{YELLOW}Advertencia: Gitleaks no se instaló correctamente. Algunos hooks pueden fallar.{RESET}"
        )

    # Instalar KICS
    if not install_kics():
        print(
            f"{YELLOW}Advertencia: KICS no se instaló correctamente. Algunos hooks pueden fallar.{RESET}"
        )

    # Instalar hooks de pre-commit
    if not install_pre_commit_hooks():
        print(f"{RED}No se pudieron instalar los hooks de pre-commit.{RESET}")
        return 1

    print_header("Instalación completada")
    print(f"{GREEN}Todas las dependencias se han instalado correctamente.{RESET}")
    print(f"Ahora puede ejecutar {BOLD}pre-commit run --all-files{RESET} para verificar su código.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
