#!/usr/bin/env python
"""
Script para revisar los falsos positivos detectados por las herramientas de seguridad.

Este script analiza los resultados de las herramientas de seguridad y ayuda a
identificar y clasificar los falsos positivos.
"""

import argparse
import json
import os
import re
import sys
from typing import Any


def load_config(config_file: str) -> dict[str, Any]:
    """
    Carga la configuración de exclusiones.

    Args:
        config_file: Ruta al archivo de configuración

    Returns:
        Diccionario con la configuración
    """
    try:
        with open(config_file, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar el archivo de configuración: {e}")
        return {"exclude_dirs": [], "exclude_files": [], "exclude_patterns": []}


def load_security_report(report_file: str) -> list[dict[str, Any]]:
    """
    Carga un informe de seguridad en formato JSON.

    Args:
        report_file: Ruta al archivo de informe

    Returns:
        Lista de hallazgos de seguridad
    """
    try:
        with open(report_file, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar el informe de seguridad: {e}")
        return []


def is_excluded(finding: dict[str, Any], config: dict[str, Any]) -> bool:
    """
    Determina si un hallazgo debe ser excluido según la configuración.

    Args:
        finding: Hallazgo de seguridad
        config: Configuración de exclusiones

    Returns:
        True si el hallazgo debe ser excluido, False en caso contrario
    """
    # Verificar si el archivo está en directorios excluidos
    file_path = finding.get("file_path", "")
    for exclude_dir in config.get("exclude_dirs", []):
        if exclude_dir in file_path:
            return True

    # Verificar si el archivo está en archivos excluidos
    for exclude_file in config.get("exclude_files", []):
        if exclude_file == os.path.basename(file_path):
            return True
        if "*" in exclude_file:
            pattern = exclude_file.replace(".", "\\.").replace("*", ".*")
            if re.match(pattern, os.path.basename(file_path)):
                return True

    # Verificar si el contenido coincide con patrones excluidos
    content = finding.get("content", "")
    for exclude_pattern in config.get("exclude_patterns", []):
        if re.search(exclude_pattern, content):
            return True

    return False


def classify_findings(
    findings: list[dict[str, Any]], config: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Clasifica los hallazgos en falsos positivos y verdaderos positivos.

    Args:
        findings: Lista de hallazgos de seguridad
        config: Configuración de exclusiones

    Returns:
        Tupla con listas de falsos positivos y verdaderos positivos
    """
    false_positives = []
    true_positives = []

    for finding in findings:
        if is_excluded(finding, config):
            false_positives.append(finding)
        else:
            true_positives.append(finding)

    return false_positives, true_positives


def generate_report(
    false_positives: list[dict[str, Any]],
    true_positives: list[dict[str, Any]],
    output_file: str | None = None,
) -> None:
    """
    Genera un informe con los falsos positivos y verdaderos positivos.

    Args:
        false_positives: Lista de falsos positivos
        true_positives: Lista de verdaderos positivos
        output_file: Archivo de salida (opcional)
    """
    output = []
    output.append("# Informe de Revisión de Falsos Positivos")
    output.append("")

    # Resumen
    output.append("## Resumen")
    output.append("")
    output.append(f"- Total de hallazgos: {len(false_positives) + len(true_positives)}")
    output.append(f"- Falsos positivos: {len(false_positives)}")
    output.append(f"- Verdaderos positivos: {len(true_positives)}")
    output.append("")

    # Verdaderos positivos
    output.append("## Verdaderos Positivos")
    output.append("")

    if true_positives:
        for i, finding in enumerate(true_positives, 1):
            output.append(f"### Hallazgo {i}")
            output.append("")
            output.append(f"- **Archivo**: {finding.get('file_path', 'N/A')}")
            output.append(f"- **Línea**: {finding.get('line_number', 'N/A')}")
            output.append(f"- **Tipo**: {finding.get('type', 'N/A')}")
            output.append(f"- **Severidad**: {finding.get('severity', 'N/A')}")
            output.append("")
            output.append("**Contenido:**")
            output.append("")
            output.append(f"```\n{finding.get('content', 'N/A')}\n```")
            output.append("")
    else:
        output.append("No se encontraron verdaderos positivos.")
        output.append("")

    # Falsos positivos
    output.append("## Falsos Positivos")
    output.append("")

    if false_positives:
        for i, finding in enumerate(false_positives, 1):
            output.append(f"### Falso Positivo {i}")
            output.append("")
            output.append(f"- **Archivo**: {finding.get('file_path', 'N/A')}")
            output.append(f"- **Línea**: {finding.get('line_number', 'N/A')}")
            output.append(f"- **Tipo**: {finding.get('type', 'N/A')}")
            output.append(f"- **Severidad**: {finding.get('severity', 'N/A')}")
            output.append("")
            output.append("**Contenido:**")
            output.append("")
            output.append(f"```\n{finding.get('content', 'N/A')}\n```")
            output.append("")
    else:
        output.append("No se encontraron falsos positivos.")
        output.append("")

    # Recomendaciones
    output.append("## Recomendaciones")
    output.append("")

    if true_positives:
        output.append("### Para Verdaderos Positivos")
        output.append("")
        output.append(
            "1. Revise cada hallazgo y determine si representa un riesgo real de seguridad."
        )
        output.append("2. Corrija los problemas de seguridad encontrados.")
        output.append(
            "3. Considere implementar pruebas automatizadas para evitar que estos problemas se repitan."
        )
        output.append("")

    if false_positives:
        output.append("### Para Falsos Positivos")
        output.append("")
        output.append(
            "1. Actualice el archivo de configuración para excluir estos falsos positivos."
        )
        output.append(
            "2. Considere agregar patrones más específicos para reducir la cantidad de falsos positivos."
        )
        output.append(
            "3. Si un patrón genera muchos falsos positivos, considere eliminarlo o refinarlo."
        )
        output.append("")

    report = "\n".join(output)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Informe guardado en {output_file}")
    else:
        print(report)


def main() -> int:
    """Función principal del script."""
    parser = argparse.ArgumentParser(
        description="Revisar falsos positivos en informes de seguridad"
    )
    parser.add_argument("--report", "-r", required=True, help="Archivo de informe de seguridad")
    parser.add_argument(
        "--config",
        "-c",
        default="scripts/security_check_config.json",
        help="Archivo de configuración",
    )
    parser.add_argument("--output", "-o", help="Archivo de salida para el informe")

    args = parser.parse_args()

    config = load_config(args.config)
    findings = load_security_report(args.report)

    if not findings:
        print(f"No se encontraron hallazgos en el informe {args.report}")
        return 0

    false_positives, true_positives = classify_findings(findings, config)
    generate_report(false_positives, true_positives, args.output)

    # Devolver código de salida 1 si hay verdaderos positivos
    return 1 if true_positives else 0


if __name__ == "__main__":
    sys.exit(main())
