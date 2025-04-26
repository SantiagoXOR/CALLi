#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def validate_puml_files():
    """Valida todos los archivos PlantUML en el directorio de diagramas."""
    diagrams_dir = Path(__file__).parent.parent / 'diagrams'
    errors = []
    
    for puml_file in diagrams_dir.glob('*.puml'):
        with open(puml_file) as f:
            content = f.read()
            
        # Validaciones básicas
        if not content.strip().startswith('@startuml'):
            errors.append(f"{puml_file}: Falta @startuml al inicio")
        if not content.strip().endswith('@enduml'):
            errors.append(f"{puml_file}: Falta @enduml al final")
            
    return errors

if __name__ == '__main__':
    errors = validate_puml_files()
    if errors:
        print("Errores encontrados en diagramas:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    print("Todos los diagramas son válidos")
