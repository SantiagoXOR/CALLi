#!/usr/bin/env python3
"""
Script para verificar los encabezados de seguridad en las respuestas HTTP.
Este script verifica que las respuestas HTTP incluyan los encabezados de seguridad recomendados.
"""

import argparse
import json
import os
import sys
from typing import Any
from urllib.parse import urlparse

import requests

# Colores para la salida en terminal
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Encabezados de seguridad recomendados y sus valores
RECOMMENDED_HEADERS = {
    "X-Content-Type-Options": ["nosniff"],
    "X-Frame-Options": ["DENY", "SAMEORIGIN"],
    "X-XSS-Protection": ["1", "1; mode=block"],
    "Content-Security-Policy": None,  # Cualquier valor es aceptable
    "Strict-Transport-Security": None,  # Cualquier valor es aceptable
    "Referrer-Policy": [
        "no-referrer",
        "no-referrer-when-downgrade",
        "origin",
        "origin-when-cross-origin",
        "same-origin",
        "strict-origin",
        "strict-origin-when-cross-origin",
    ],
    "Permissions-Policy": None,  # Cualquier valor es aceptable
}


def check_url(url: str) -> dict[str, Any]:
    """
    Verifica los encabezados de seguridad de una URL.

    Args:
        url: La URL a verificar

    Returns:
        Un diccionario con los resultados de la verificación
    """
    result = {
        "url": url,
        "status": "unknown",
        "status_code": None,
        "headers": {},
        "missing_headers": [],
        "insecure_headers": [],
        "score": 0,
        "max_score": len(RECOMMENDED_HEADERS),
    }

    try:
        # Verificar si la URL es válida
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            result["status"] = "error"
            result["error"] = "URL inválida"
            return result

        # Realizar la solicitud HTTP
        response = requests.get(url, timeout=10, allow_redirects=True)
        result["status_code"] = response.status_code

        if response.status_code >= 400:
            result["status"] = "error"
            result["error"] = f"Error HTTP {response.status_code}"
            return result

        # Verificar los encabezados de seguridad
        headers = {k.lower(): v for k, v in response.headers.items()}
        result["headers"] = dict(response.headers)

        for header, valid_values in RECOMMENDED_HEADERS.items():
            header_lower = header.lower()

            if header_lower in headers:
                # El encabezado está presente
                if valid_values is None:
                    # Cualquier valor es aceptable
                    result["score"] += 1
                elif headers[header_lower] in valid_values:
                    # El valor es aceptable
                    result["score"] += 1
                else:
                    # El valor no es aceptable
                    result["insecure_headers"].append(
                        {
                            "header": header,
                            "value": headers[header_lower],
                            "recommended": valid_values,
                        }
                    )
            else:
                # El encabezado no está presente
                result["missing_headers"].append(header)

        # Calcular el estado general
        if result["score"] == result["max_score"]:
            result["status"] = "secure"
        elif result["score"] >= result["max_score"] * 0.7:
            result["status"] = "warning"
        else:
            result["status"] = "insecure"

        return result
    except requests.exceptions.RequestException as e:
        result["status"] = "error"
        result["error"] = f"Error de conexión: {e!s}"
        return result
    except Exception as e:
        result["status"] = "error"
        result["error"] = f"Error inesperado: {e!s}"
        return result


def generate_markdown_report(results: list[dict[str, Any]]) -> str:
    """
    Genera un informe en formato Markdown con los resultados de la verificación.

    Args:
        results: Lista de resultados de verificación

    Returns:
        El informe en formato Markdown
    """
    report = "# Informe de Encabezados de Seguridad\n\n"

    for result in results:
        url = result["url"]
        status = result["status"]

        if status == "secure":
            status_text = f"🟢 **Seguro** ({result['score']}/{result['max_score']})"
        elif status == "warning":
            status_text = f"🟡 **Advertencia** ({result['score']}/{result['max_score']})"
        elif status == "insecure":
            status_text = f"🔴 **Inseguro** ({result['score']}/{result['max_score']})"
        else:
            status_text = f"⚠️ **Error**: {result.get('error', 'Desconocido')}"

        report += f"## {url}\n\n"
        report += f"Estado: {status_text}\n\n"

        if status != "error":
            if result["missing_headers"]:
                report += "### Encabezados faltantes\n\n"
                for header in result["missing_headers"]:
                    report += f"- `{header}`\n"
                report += "\n"

            if result["insecure_headers"]:
                report += "### Encabezados inseguros\n\n"
                for item in result["insecure_headers"]:
                    header = item["header"]
                    value = item["value"]
                    recommended = (
                        ", ".join(f"`{r}`" for r in item["recommended"])
                        if item["recommended"]
                        else "Cualquier valor"
                    )

                    report += f"- `{header}`: `{value}`\n"
                    report += f"  - Valores recomendados: {recommended}\n"
                report += "\n"

            report += "### Todos los encabezados\n\n"
            report += "```\n"
            for header, value in result["headers"].items():
                report += f"{header}: {value}\n"
            report += "```\n\n"

        report += "---\n\n"

    report += "## Recomendaciones\n\n"
    report += "Para mejorar la seguridad de tu sitio web, asegúrate de incluir los siguientes encabezados:\n\n"

    for header, valid_values in RECOMMENDED_HEADERS.items():
        if valid_values:
            values_text = ", ".join(f"`{v}`" for v in valid_values)
            report += f"- `{header}`: {values_text}\n"
        else:
            report += f"- `{header}`: Cualquier valor apropiado\n"

    return report


def main() -> int:
    """Función principal."""
    parser = argparse.ArgumentParser(
        description="Verificar encabezados de seguridad en respuestas HTTP"
    )
    parser.add_argument("--urls", help="Lista de URLs separadas por comas para verificar")
    parser.add_argument("--output", help="Archivo de salida para los resultados (JSON)")
    parser.add_argument("--report", help="Archivo de salida para el informe (Markdown)")
    args = parser.parse_args()

    # Obtener las URLs de los argumentos o de las variables de entorno
    urls_str = args.urls or os.environ.get("CHECK_URLS", "")
    if not urls_str:
        print(f"{RED}Error: No se especificaron URLs para verificar{RESET}")
        print(
            "Uso: python check_security_headers.py --urls=https://example.com,https://example.org"
        )
        return 1

    urls = [url.strip() for url in urls_str.split(",") if url.strip()]

    if not urls:
        print(f"{RED}Error: No se especificaron URLs válidas{RESET}")
        return 1

    print(f"{BOLD}Verificando encabezados de seguridad para {len(urls)} URL(s)...{RESET}")

    results = []
    for url in urls:
        print(f"Verificando {url}...")
        result = check_url(url)
        results.append(result)

        if result["status"] == "secure":
            print(f"  {GREEN}✓ Seguro ({result['score']}/{result['max_score']}){RESET}")
        elif result["status"] == "warning":
            print(f"  {YELLOW}⚠ Advertencia ({result['score']}/{result['max_score']}){RESET}")
        elif result["status"] == "insecure":
            print(f"  {RED}✗ Inseguro ({result['score']}/{result['max_score']}){RESET}")
        else:
            print(f"  {RED}✗ Error: {result.get('error', 'Desconocido')}{RESET}")

    # Guardar los resultados en formato JSON
    output_file = args.output or "security_headers_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nResultados guardados en {output_file}")

    # Generar y guardar el informe en formato Markdown
    report_file = args.report or "security_headers_report.md"
    report = generate_markdown_report(results)
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Informe guardado en {report_file}")

    # Determinar el código de salida
    if any(result["status"] == "insecure" for result in results):
        print(f"\n{RED}⚠ Se encontraron problemas de seguridad en los encabezados HTTP{RESET}")
        return 1
    if any(result["status"] == "warning" for result in results):
        print(f"\n{YELLOW}⚠ Se encontraron advertencias en los encabezados HTTP{RESET}")
        return 0
    if any(result["status"] == "error" for result in results):
        print(f"\n{RED}⚠ Se produjeron errores al verificar los encabezados HTTP{RESET}")
        return 1
    print(f"\n{GREEN}✓ Todos los encabezados HTTP son seguros{RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
