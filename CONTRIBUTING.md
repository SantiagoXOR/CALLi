# Guía de Contribución

## Estándares de Código

### Python (Backend)
- Usar type hints en todas las funciones
- Documentar funciones con docstrings
- Seguir PEP 8
- Máximo 100 caracteres por línea
- Usar f-strings para formateo

### TypeScript (Frontend)
- Usar tipos explícitos
- No usar 'any'
- Componentes funcionales con tipos Props
- Imports organizados por grupos
- Nombres descriptivos para componentes

## Proceso de Desarrollo
1. Crear rama feature/fix
2. Ejecutar validaciones locales
3. Crear PR con descripción detallada
4. Esperar revisión y CI
5. Mergear después de aprobación

## Comandos Útiles
```bash
# Validar todo el proyecto
./scripts/validate.sh

# Instalar pre-commit hooks
pre-commit install

# Actualizar dependencias
pip install -e ".[test]"
cd frontend-call-automation && npm install
