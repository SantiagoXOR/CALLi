# Guía de Calidad de Código

## Métricas y Umbrales

### Python
- Cobertura de código: mínimo 80%
- Complejidad ciclomática máxima: 10
- Longitud máxima de línea: 100 caracteres
- Cobertura de tipos: 100%

### TypeScript
- No any permitido
- Imports ordenados
- Props tipados explícitamente
- Tests unitarios requeridos para componentes

## Proceso de Verificación

1. **Verificación Local**
   ```bash
   # Ejecutar auditoría completa
   python scripts/quality_audit.py

   # Verificar cobertura
   pytest --cov=app --cov-report=html
   ```

2. **Pre-commit**
   Los hooks verificarán:
   - Formato de código
   - Imports no utilizados
   - Tipos
   - Reglas de linting

3. **CI/CD**
   Cada PR debe pasar:
   - Auditoría de calidad
   - Tests unitarios
   - Escaneo de seguridad
   - Verificación de dependencias

## Mantenimiento

- Ejecutar auditoría semanal de dependencias
- Actualizar reglas de linting mensualmente
- Revisar y actualizar umbrales de calidad trimestralmente
