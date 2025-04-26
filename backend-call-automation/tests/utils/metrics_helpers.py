"""
Utilidades para pruebas relacionadas con métricas.
"""
import re
from typing import Dict, Any, List, Optional


def parse_metrics_text(metrics_text: str) -> Dict[str, Any]:
    """
    Parsea el texto de métricas de Prometheus a un diccionario.
    
    Args:
        metrics_text: Texto de métricas en formato Prometheus
        
    Returns:
        Diccionario con las métricas parseadas
    """
    metrics = {}
    lines = metrics_text.strip().split('\n')
    
    current_metric = None
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Si es una nueva métrica (no tiene espacios al inicio)
        if not line.startswith(' '):
            parts = line.split(' ', 1)
            if len(parts) == 2:
                metric_name, value = parts
                try:
                    metrics[metric_name] = float(value)
                except ValueError:
                    metrics[metric_name] = value
                current_metric = metric_name
        # Si es parte de una métrica existente (tiene espacios al inicio)
        elif current_metric and line.startswith(' '):
            if current_metric not in metrics:
                metrics[current_metric] = []
            metrics[current_metric].append(line.strip())
    
    return metrics


def assert_metric_present(metrics: Dict[str, Any], metric_name: str) -> bool:
    """
    Verifica que una métrica esté presente en el diccionario de métricas.
    
    Args:
        metrics: Diccionario de métricas
        metric_name: Nombre de la métrica a verificar
        
    Returns:
        True si la métrica está presente, False en caso contrario
    """
    return metric_name in metrics


def assert_metric_value(metrics: Dict[str, Any], metric_name: str, expected_value: Any) -> bool:
    """
    Verifica que una métrica tenga el valor esperado.
    
    Args:
        metrics: Diccionario de métricas
        metric_name: Nombre de la métrica a verificar
        expected_value: Valor esperado
        
    Returns:
        True si la métrica tiene el valor esperado, False en caso contrario
    """
    if not assert_metric_present(metrics, metric_name):
        return False
    
    # Convertir a float si es posible para comparación numérica
    if isinstance(metrics[metric_name], (int, float)) and isinstance(expected_value, (int, float)):
        return abs(float(metrics[metric_name]) - float(expected_value)) < 0.0001
    
    return metrics[metric_name] == expected_value


def extract_metric_labels(metric_line: str) -> Dict[str, str]:
    """
    Extrae las etiquetas de una línea de métrica.
    
    Args:
        metric_line: Línea de métrica con etiquetas
        
    Returns:
        Diccionario con las etiquetas extraídas
    """
    labels = {}
    match = re.search(r'{(.+?)}', metric_line)
    if match:
        labels_str = match.group(1)
        for label_pair in labels_str.split(','):
            if '=' in label_pair:
                key, value = label_pair.split('=', 1)
                labels[key.strip()] = value.strip().strip('"')
    return labels


def find_metric_with_labels(metrics_text: str, metric_name: str, labels: Dict[str, str]) -> Optional[float]:
    """
    Busca una métrica con etiquetas específicas y devuelve su valor.
    
    Args:
        metrics_text: Texto de métricas en formato Prometheus
        metric_name: Nombre de la métrica a buscar
        labels: Diccionario de etiquetas a buscar
        
    Returns:
        Valor de la métrica si se encuentra, None en caso contrario
    """
    lines = metrics_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if line.startswith(f"{metric_name}{{"):
            line_labels = extract_metric_labels(line)
            
            # Verificar si todas las etiquetas buscadas están presentes
            match = True
            for key, value in labels.items():
                if key not in line_labels or line_labels[key] != value:
                    match = False
                    break
            
            if match:
                # Extraer el valor
                value_match = re.search(r'} (\d+(\.\d+)?)', line)
                if value_match:
                    return float(value_match.group(1))
    
    return None
