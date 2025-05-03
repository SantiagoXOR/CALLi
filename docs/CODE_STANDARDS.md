# Estándares de Código

Este documento define los estándares de código para el proyecto CALLi. Seguir estos estándares asegura la consistencia, legibilidad y mantenibilidad del código.

## Estilo de Código

### PEP 8

Seguimos las recomendaciones de [PEP 8](https://www.python.org/dev/peps/pep-0008/), el estándar de estilo para código Python, con algunas adaptaciones específicas para nuestro proyecto.

### Herramientas de Formateo

Utilizamos las siguientes herramientas para mantener la consistencia del código:

- **Black**: Para formateo automático de código
- **isort**: Para ordenar importaciones
- **Ruff**: Para linting y detección de errores

Configuración recomendada en `pyproject.toml`:

```toml
[tool.black]
line-length = 88
target-version = ['py310']
include = '\.pyi?$'

[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3

[tool.ruff]
line-length = 88
target-version = "py310"
select = ["E", "F", "B", "I"]
ignore = ["E203"]
```

## Convenciones de Nomenclatura

### Archivos y Directorios

- Usar minúsculas con guiones bajos (snake_case)
- Ejemplos: `call_service.py`, `user_authentication.py`

### Clases

- Usar CamelCase (primera letra mayúscula)
- Ejemplos: `CallService`, `UserAuthentication`

### Funciones y Variables

- Usar minúsculas con guiones bajos (snake_case)
- Ejemplos: `get_user_by_id()`, `active_users`

### Constantes

- Usar mayúsculas con guiones bajos
- Ejemplos: `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`

### Nombres Descriptivos

- Usar nombres descriptivos que indiquen el propósito
- Evitar abreviaturas no estándar
- Preferir nombres explícitos sobre nombres cortos pero ambiguos

## Estructura de Archivos

### Encabezado de Archivo

Cada archivo debe comenzar con un docstring que describa su propósito:

```python
"""
Módulo para la gestión de llamadas.

Este módulo proporciona funcionalidades para crear, gestionar y monitorear
llamadas telefónicas a través de la integración con Twilio.
"""
```

### Orden de Elementos

1. Docstring del módulo
2. Importaciones (ver sección de importaciones)
3. Constantes
4. Clases y funciones
5. Código de inicialización (si es necesario)
6. Bloque `if __name__ == "__main__"` (si es necesario)

### Longitud de Archivos

- Mantener archivos por debajo de 500 líneas cuando sea posible
- Dividir archivos grandes en módulos más pequeños y cohesivos

## Convenciones de Importación

### Orden de Importaciones

1. Importaciones de biblioteca estándar
2. Importaciones de terceros
3. Importaciones del proyecto
4. Importaciones relativas

Ejemplo:

```python
# Importaciones de biblioteca estándar
import os
import json
from typing import List, Dict, Optional

# Importaciones de terceros
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field

# Importaciones del proyecto
from app.dependencies import get_db
from app.models.user import User
from app.utils.logging import logger

# Importaciones relativas (solo para módulos en el mismo paquete)
from .schemas import UserCreate
```

### Estándar de Importaciones para Dependencias

Para mantener la consistencia en todo el proyecto, hemos establecido el siguiente estándar para importar dependencias:

1. **Dependencias de Servicio**:
   ```python
   from app.dependencies import get_call_service, CallServiceDep
   ```

2. **Dependencias de Configuración**:
   ```python
   from app.config.dependencies import get_supabase_client
   ```

3. **No mezclar ambos tipos de importaciones**:
   Mantener clara la distinción entre dependencias de servicio y configuración.

### Importaciones Absolutas vs. Relativas

- Preferir importaciones absolutas para claridad y evitar ambigüedades
- Usar importaciones relativas solo para módulos en el mismo paquete
- Evitar importaciones relativas que suban más de un nivel (`from ...module import x`)

## Documentación de Código

### Docstrings

Usamos el formato de docstring de Google para documentar funciones, clases y métodos:

```python
def get_user_by_id(user_id: int) -> Optional[User]:
    """
    Obtiene un usuario por su ID.

    Args:
        user_id: ID del usuario a buscar

    Returns:
        Usuario encontrado o None si no existe

    Raises:
        ValueError: Si el ID de usuario es negativo
    """
```

### Comentarios

- Usar comentarios para explicar "por qué", no "qué"
- Mantener los comentarios actualizados con el código
- Evitar comentarios obvios que no añaden valor

## Manejo de Errores

### Excepciones

- Usar excepciones específicas en lugar de excepciones genéricas
- Documentar las excepciones que puede lanzar una función
- Manejar excepciones en el nivel apropiado

Ejemplo:

```python
try:
    result = service.process_data(data)
except ValidationError as e:
    logger.warning(f"Datos inválidos: {e}")
    raise HTTPException(status_code=400, detail=str(e))
except ServiceUnavailableError as e:
    logger.error(f"Servicio no disponible: {e}")
    raise HTTPException(status_code=503, detail="Servicio temporalmente no disponible")
```

### Logging

- Usar niveles de log apropiados (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Incluir información contextual relevante en los mensajes de log
- Evitar loggear información sensible

## Pruebas

### Nomenclatura de Pruebas

- Archivos de prueba: `test_*.py`
- Funciones de prueba: `test_*`
- Clases de prueba: `Test*`

### Estructura de Pruebas

- Una prueba debe verificar un solo aspecto o comportamiento
- Usar fixtures para configuración común
- Seguir el patrón AAA (Arrange, Act, Assert)

Ejemplo:

```python
def test_get_user_by_id_existing_user():
    # Arrange
    user_id = 1
    expected_user = User(id=1, name="Test User")
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = expected_user

    # Act
    result = get_user_by_id(user_id, db=mock_db)

    # Assert
    assert result == expected_user
```

## Seguridad

### Datos Sensibles

- No hardcodear secretos o credenciales en el código
- Usar variables de entorno o servicios de gestión de secretos
- Enmascarar datos sensibles en logs

### Validación de Entrada

- Validar todas las entradas de usuario
- Usar esquemas Pydantic para validación automática
- Implementar validaciones adicionales cuando sea necesario

## Rendimiento

### Optimización

- Optimizar solo cuando sea necesario, basado en mediciones
- Documentar optimizaciones complejas
- Considerar el impacto en la legibilidad y mantenibilidad

### Recursos

- Liberar recursos explícitamente (conexiones de base de datos, archivos, etc.)
- Usar manejadores de contexto (`with`) cuando sea posible
- Considerar el uso de memoria y CPU en operaciones costosas

## Control de Versiones

### Mensajes de Commit

Formato recomendado:

```
[Tipo] Descripción corta (50 caracteres o menos)

Descripción más detallada si es necesario. Mantener las líneas
a 72 caracteres o menos. La línea en blanco que separa el resumen
del cuerpo es crítica.
```

Tipos comunes:
- `[Feature]`: Nueva funcionalidad
- `[Fix]`: Corrección de errores
- `[Refactor]`: Refactorización de código
- `[Docs]`: Cambios en documentación
- `[Test]`: Adición o modificación de pruebas
- `[Chore]`: Tareas de mantenimiento

### Ramas

- `master`: Código de producción
- `develop`: Código de desarrollo integrado
- `feature/*`: Nuevas características
- `bugfix/*`: Correcciones de errores
- `hotfix/*`: Correcciones urgentes para producción

## Revisión de Código

### Criterios de Revisión

- El código sigue los estándares definidos
- Las pruebas cubren adecuadamente la funcionalidad
- La documentación está actualizada
- No hay problemas de seguridad evidentes
- El código es eficiente y mantenible

### Proceso de Revisión

1. El autor crea un Pull Request (PR)
2. Al menos un revisor aprueba el PR
3. CI/CD pasa todas las verificaciones
4. El autor o un mantenedor fusiona el PR
