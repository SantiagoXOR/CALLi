"""Helpers para pruebas de métricas Prometheus."""

import re
from typing import Dict, Optional, Union

def parse_metrics_text(metrics_text: str) -> Dict[str, dict]:
    """
    Parsea texto plano de métricas Prometheus en un diccionario estructurado.
    
    Args:
        metrics_text: Texto plano de respuesta de /metrics
        
    Returns:
        Dict with metric names as keys containing:
        - type: Metric type (counter, gauge, etc)
        - help: Description
        - samples: List of samples with value and labels
    """
    metrics = {}
    current_metric = None
    
    for line in metrics_text.split('\n'):
        if line.startswith('# TYPE'):
            parts = line.split()
            current_metric = parts[2]
            metrics[current_metric] = {
                'type': parts[3],
                'help': '',
                'samples': []
            }
        elif line.startswith('# HELP'):
            parts = line.split()
            metric_name = parts[2]
            if metric_name in metrics:
                metrics[metric_name]['help'] = ' '.join(parts[3:])
        elif line and not line.startswith('#'):
            if current_metric and current_metric in metrics:
                if '{' in line:  # Metric with labels
                    name, rest = line.split('{', 1)
                    labels_part, value_part = rest.rsplit('}', 1)
                    value = float(value_part.strip().split()[1])
                    labels = {}
                    for label in labels_part.split(','):
                        k, v = label.strip().split('=')
                        labels[k] = v.strip('"')
                    metrics[current_metric]['samples'].append({
                        'value': value,
                        'labels': labels
                    })
                else:  # Metric without labels
                    parts = line.split()
                    value = float(parts[1])
                    metrics[current_metric]['samples'].append({
                        'value': value,
                        'labels': {}
                    })
                    
    return metrics

def assert_metric_present(
    metrics_data: Dict[str, dict], 
    metric_name: str,
    labels: Optional[Dict[str, str]] = None
) -> bool:
    """
    Verifica si una métrica con labels específicos está presente.
    
    Args:
        metrics_data: Output from parse_metrics_text()
        metric_name: Name of metric to check
        labels: Expected labels (None means any labels)
        
    Returns:
        True if metric with matching labels exists
    """
    if metric_name not in metrics_data:
        return False
        
    if labels is None:
        return len(metrics_data[metric_name]['samples']) > 0
        
    for sample in metrics_data[metric_name]['samples']:
        match = True
        for k, v in labels.items():
            if k not in sample['labels'] or sample['labels'][k] != v:
                match = False
                break
        if match:
            return True
            
    return False

def assert_metric_value(
    metrics_data: Dict[str, dict],
    metric_name: str,
    expected_value: Union[int, float],
    labels: Optional[Dict[str, str]] = None,
    delta: float = 0.001
) -> bool:
    """
    Verifica si una métrica tiene un valor específico.
    
    Args:
        metrics_data: Output from parse_metrics_text()
        metric_name: Name of metric to check
        expected_value: Expected numeric value
        labels: Expected labels (None means any labels)
        delta: Allowed difference for floating point comparison
        
    Returns:
        True if metric with matching labels has value within delta
    """
    if metric_name not in metrics_data:
        return False
        
    for sample in metrics_data[metric_name]['samples']:
        match = True
        if labels is not None:
            for k, v in labels.items():
                if k not in sample['labels'] or sample['labels'][k] != v:
                    match = False
                    break
        if match and abs(sample['value'] - expected_value) <= delta:
            return True
            
    return False
