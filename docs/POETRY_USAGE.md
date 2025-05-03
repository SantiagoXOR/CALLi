# Uso de Poetry para Gestión de Dependencias

Este proyecto utiliza [Poetry](https://python-poetry.org/) para la gestión de dependencias. Poetry proporciona un sistema robusto para gestionar dependencias, entornos virtuales y empaquetado de proyectos Python.

## Instalación de Poetry

### En Windows
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### En macOS/Linux
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## Configuración Inicial

Después de instalar Poetry, navega al directorio del proyecto y ejecuta:

```bash
# Inicializar el proyecto (solo si no existe pyproject.toml)
poetry init

# Instalar dependencias desde pyproject.toml
poetry install
```

## Comandos Básicos

### Instalar Dependencias
```bash
# Instalar todas las dependencias (incluidas las de desarrollo)
poetry install

# Instalar solo dependencias de producción (sin las de desarrollo)
poetry install --no-dev
```

### Agregar Dependencias
```bash
# Agregar una dependencia de producción
poetry add fastapi

# Agregar una dependencia de desarrollo
poetry add --group dev pytest

# Agregar una dependencia con una versión específica
poetry add "fastapi>=0.89.1"

# Agregar una dependencia con extras
poetry add "uvicorn[standard]"
```

### Actualizar Dependencias
```bash
# Actualizar todas las dependencias
poetry update

# Actualizar una dependencia específica
poetry update fastapi
```

### Eliminar Dependencias
```bash
# Eliminar una dependencia
poetry remove fastapi
```

### Activar el Entorno Virtual
```bash
# Activar el entorno virtual
poetry shell

# Ejecutar un comando en el entorno virtual sin activarlo
poetry run python -m pytest
```

### Exportar Dependencias
```bash
# Exportar a requirements.txt
poetry export -f requirements.txt --output requirements.txt

# Exportar incluyendo dependencias de desarrollo
poetry export -f requirements.txt --output requirements-dev.txt --with dev
```

## Estructura del Archivo pyproject.toml

El archivo `pyproject.toml` contiene la configuración del proyecto y sus dependencias:

```toml
[tool.poetry]
name = "call-automation"
version = "0.1.0"
description = "Sistema de automatización de llamadas telefónicas"
authors = ["Santiago Martinez <santiago@xor.com.ar>"]
readme = "README.md"
packages = [{include = "app"}]

[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.89.1"
# Otras dependencias...

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
# Otras dependencias de desarrollo...

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## Archivo poetry.lock

El archivo `poetry.lock` contiene las versiones exactas de todas las dependencias y sus subdependencias. Este archivo debe ser versionado para garantizar que todos los desarrolladores y entornos utilicen exactamente las mismas versiones.

## Migración desde requirements.txt

Si estás migrando desde un proyecto que utiliza `requirements.txt`, puedes convertirlo a Poetry con:

```bash
# Crear un nuevo proyecto Poetry
poetry init

# Instalar dependencias desde requirements.txt
poetry add $(cat requirements.txt)
```

## Integración con CI/CD

Para integrar Poetry con GitHub Actions, puedes usar:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Poetry
        uses: snok/install-poetry@v1
        with:
          version: 1.5.1

      - name: Install dependencies
        run: poetry install

      - name: Run tests
        run: poetry run pytest
```

## Ventajas de Poetry sobre pip/requirements.txt

1. **Resolución de Dependencias**: Poetry resuelve automáticamente las dependencias y sus conflictos.
2. **Bloqueo de Versiones**: El archivo `poetry.lock` garantiza que todos usen exactamente las mismas versiones.
3. **Grupos de Dependencias**: Separación clara entre dependencias de producción y desarrollo.
4. **Entorno Virtual Integrado**: Gestión automática de entornos virtuales.
5. **Publicación Simplificada**: Facilita la publicación de paquetes en PyPI.
6. **Interfaz Consistente**: Comandos intuitivos y consistentes.
