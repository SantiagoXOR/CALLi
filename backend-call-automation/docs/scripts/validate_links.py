#!/usr/bin/env python3
import os
import re
from pathlib import Path

def validate_internal_links():
    """Valida enlaces internos en archivos RST."""
    docs_dir = Path(__file__).parent.parent
    errors = []
    refs = set()
    links = set()
    
    # Recolectar todas las referencias y enlaces
    for rst_file in docs_dir.rglob('*.rst'):
        with open(rst_file) as f:
            content = f.read()
            
        # Encontrar referencias
        refs.update(re.findall(r'^\.\. _([^:]+):', content, re.MULTILINE))
        # Encontrar enlaces
        links.update(re.findall(r':ref:`([^`]+)`', content))
    
    # Validar enlaces
    for link in links:
        if link not in refs:
            errors.append(f"Enlace roto: {link}")
    
    return errors

if __name__ == '__main__':
    errors = validate_internal_links()
    if errors:
        print("Errores encontrados en enlaces:")
        for error in errors:
            print(f"- {error}")
        exit(1)
    print("Todos los enlaces son válidos")
