#!/usr/bin/env python3
"""
Script para ejecutar los tests del proyecto.
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path

def main():
    """Ejecuta los tests del proyecto."""
    parser = argparse.ArgumentParser(description="Ejecuta los tests del proyecto")
    parser.add_argument("--backend", action="store_true", help="Ejecutar solo tests de backend")
    parser.add_argument("--frontend", action="store_true", help="Ejecutar solo tests de frontend")
    parser.add_argument("--coverage", action="store_true", help="Generar reporte de cobertura")
    parser.add_argument("--verbose", "-v", action="store_true", help="Modo verboso")
    parser.add_argument("--pattern", "-p", type=str, help="Patrón para filtrar tests")
    args = parser.parse_args()

    # Obtener el directorio raíz del proyecto
    root_dir = Path(__file__).parent.parent.absolute()
    
    # Si no se especifica ninguna opción, ejecutar todos los tests
    if not args.backend and not args.frontend:
        args.backend = True
        args.frontend = True
    
    exit_code = 0
    
    # Ejecutar tests de backend
    if args.backend:
        print("=== Ejecutando tests de backend ===")
        backend_cmd = ["pytest"]
        
        # Añadir opciones
        if args.verbose:
            backend_cmd.append("-v")
        
        if args.coverage:
            backend_cmd.extend(["--cov=app", "--cov-report=term", "--cov-report=xml:coverage-backend.xml"])
        
        if args.pattern:
            backend_cmd.append(args.pattern)
        else:
            backend_cmd.append("tests/")
        
        # Ejecutar pytest
        print(f"Ejecutando: {' '.join(backend_cmd)}")
        backend_result = subprocess.run(backend_cmd, cwd=root_dir)
        
        if backend_result.returncode != 0:
            exit_code = backend_result.returncode
            print("❌ Tests de backend fallidos")
        else:
            print("✅ Tests de backend exitosos")
    
    # Ejecutar tests de frontend
    if args.frontend:
        print("\n=== Ejecutando tests de frontend ===")
        frontend_dir = root_dir / "frontend-call-automation"
        
        if not frontend_dir.exists():
            print("⚠️ Directorio de frontend no encontrado, omitiendo tests")
        else:
            # Determinar si usar npm, yarn o bun
            if (frontend_dir / "bun.lockb").exists():
                cmd_prefix = ["bun", "run"]
            elif (frontend_dir / "yarn.lock").exists():
                cmd_prefix = ["yarn"]
            else:
                cmd_prefix = ["npm", "run"]
            
            frontend_cmd = cmd_prefix + ["test"]
            
            # Añadir opciones
            if args.coverage:
                frontend_cmd.append("--coverage")
            
            # Ejecutar tests de frontend
            print(f"Ejecutando: {' '.join(frontend_cmd)}")
            frontend_result = subprocess.run(frontend_cmd, cwd=frontend_dir)
            
            if frontend_result.returncode != 0:
                exit_code = frontend_result.returncode
                print("❌ Tests de frontend fallidos")
            else:
                print("✅ Tests de frontend exitosos")
    
    # Resumen final
    print("\n=== Resumen de tests ===")
    if exit_code == 0:
        print("✅ Todos los tests han pasado correctamente")
    else:
        print(f"❌ Algunos tests han fallado (código de salida: {exit_code})")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
