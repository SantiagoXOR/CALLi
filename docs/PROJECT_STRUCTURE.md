# Estructura del Proyecto y Convenciones

## Estructura de Directorios

El proyecto CALLi está organizado en los siguientes directorios principales:

```
CALLi/
├── .github/                    # Configuración de GitHub y workflows de CI/CD
├── backend-call-automation/    # Backend de la aplicación
│   ├── app/                    # Código principal de la aplicación
│   │   ├── api/                # Definiciones de API y endpoints WebSocket
│   │   │   └── endpoints/      # Endpoints específicos
│   │   ├── config/             # Configuración de la aplicación
│   │   │   ├── ai_config.py    # Configuración de servicios de IA
│   │   │   ├── dependencies.py # Dependencias de configuración
│   │   │   ├── settings.py     # Configuración general de la aplicación
│   │   │   └── supabase.py     # Configuración de Supabase
│   │   ├── dependencies/       # Dependencias e inyección de dependencias
│   │   │   ├── __init__.py     # Exporta todas las dependencias
│   │   │   └── service_dependencies.py # Dependencias de servicios
│   │   ├── middleware/         # Middleware de FastAPI
│   │   │   ├── auth.py         # Middleware de autenticación
│   │   │   └── error_handling.py # Manejo de errores
│   │   ├── models/             # Modelos de datos
│   │   │   ├── call.py         # Modelo para llamadas
│   │   │   ├── campaign.py     # Modelo para campañas
│   │   │   └── contact.py      # Modelo para contactos
│   │   ├── routers/            # Routers de FastAPI
│   │   │   ├── call_router.py  # Router para llamadas
│   │   │   ├── campaign_router.py # Router para campañas
│   │   │   └── contact_router.py # Router para contactos
│   │   ├── schemas/            # Esquemas Pydantic
│   │   │   ├── call.py         # Esquemas para llamadas
│   │   │   ├── campaign.py     # Esquemas para campañas
│   │   │   └── contact.py      # Esquemas para contactos
│   │   ├── services/           # Servicios de negocio
│   │   │   ├── call_service.py # Servicio para llamadas
│   │   │   ├── campaign_service.py # Servicio para campañas
│   │   │   └── contact_service.py # Servicio para contactos
│   │   └── utils/              # Utilidades
│   │       ├── logging.py      # Configuración de logging
│   │       └── validators.py   # Validadores personalizados
│   ├── docs/                   # Documentación específica del backend
│   ├── scripts/                # Scripts de utilidad
│   │   ├── security_check_local.py # Verificación de seguridad local
│   │   └── setup_env.py        # Configuración del entorno
│   └── tests/                  # Pruebas
│       ├── conftest.py         # Configuración de pytest
│       ├── test_routers/       # Pruebas para routers
│       ├── test_services/      # Pruebas para servicios
│       └── test_models/        # Pruebas para modelos
├── frontend-call-automation/   # Frontend de la aplicación
├── docs/                       # Documentación general del proyecto
└── scripts/                    # Scripts a nivel de proyecto
```

## Convenciones de Código

### Convenciones de Nomenclatura

1. **Archivos y Directorios**:
   - Nombres en minúsculas con guiones bajos (snake_case)
   - Ejemplos: `call_service.py`, `error_handling.py`

2. **Clases**:
   - Nombres en CamelCase
   - Ejemplos: `CallService`, `ContactModel`

3. **Funciones y Variables**:
   - Nombres en minúsculas con guiones bajos (snake_case)
   - Ejemplos: `get_call_by_id()`, `active_campaigns`

4. **Constantes**:
   - Nombres en mayúsculas con guiones bajos
   - Ejemplos: `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`

### Convenciones de Importación

1. **Orden de Importaciones**:
   ```python
   # 1. Importaciones de biblioteca estándar
   import os
   import json
   from typing import List, Dict

   # 2. Importaciones de terceros
   from fastapi import FastAPI, Depends
   from pydantic import BaseModel

   # 3. Importaciones del proyecto
   from app.dependencies import get_db
   from app.models.user import User
   ```

2. **Importaciones de Dependencias**:
   - Para dependencias de servicio: `from app.dependencies import ...`
   - Para dependencias de configuración: `from app.config.dependencies import ...`

3. **Importaciones Absolutas vs. Relativas**:
   - Preferir importaciones absolutas para claridad
   - Usar importaciones relativas solo para módulos en el mismo paquete

### Estructura de Archivos

1. **Archivos de Servicio**:
   ```python
   """
   Descripción del servicio.

   Este módulo contiene la lógica de negocio para...
   """

   # Importaciones

   # Constantes

   # Clase principal
   class MiServicio:
       """Documentación de la clase."""

       def __init__(self, dependencia):
           """Inicialización."""
           self.dependencia = dependencia

       async def metodo_principal(self, parametro):
           """Documentación del método."""
           # Implementación
   ```

2. **Archivos de Router**:
   ```python
   """
   Router para X.

   Este módulo define los endpoints para...
   """

   # Importaciones

   # Crear router
   router = APIRouter(prefix="/api/x", tags=["x"])

   # Definir endpoints
   @router.get("/")
   async def get_all():
       """Documentación del endpoint."""
       # Implementación
   ```

## Convenciones de Documentación

1. **Docstrings**:
   - Usar docstrings de triple comilla para módulos, clases y funciones
   - Incluir descripción, parámetros, retorno y excepciones

2. **Comentarios**:
   - Usar comentarios para explicar "por qué", no "qué"
   - Mantener los comentarios actualizados con el código

3. **README y Documentación**:
   - Cada directorio principal debe tener un README.md
   - La documentación detallada debe estar en el directorio `docs/`

## Convenciones de Pruebas

1. **Nomenclatura**:
   - Archivos de prueba: `test_*.py`
   - Funciones de prueba: `test_*`

2. **Estructura**:
   - Organizar pruebas por módulo/componente
   - Usar fixtures de pytest para configuración común

3. **Cobertura**:
   - Aspirar a una cobertura de pruebas del 80% o superior
   - Priorizar la cobertura de la lógica de negocio crítica

## Convenciones de Git

1. **Ramas**:
   - `master`: Código de producción
   - `develop`: Código de desarrollo integrado
   - `feature/*`: Nuevas características
   - `bugfix/*`: Correcciones de errores
   - `hotfix/*`: Correcciones urgentes para producción

2. **Commits**:
   - Mensajes claros y descriptivos
   - Formato: `[Tipo] Descripción corta`
   - Tipos: `[Feature]`, `[Fix]`, `[Refactor]`, `[Docs]`, `[Test]`

3. **Pull Requests**:
   - Incluir descripción clara de los cambios
   - Referenciar issues relacionados
   - Solicitar revisión de al menos un miembro del equipo
