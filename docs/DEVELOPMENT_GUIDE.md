# Guía de Desarrollo

## Configuración del Entorno de Desarrollo

### Requisitos Previos

- Python 3.10 o superior
- Node.js 18 o superior
- Git
- Docker y Docker Compose (opcional, para desarrollo con contenedores)

### Configuración Inicial

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/SantiagoXOR/CALLi.git
   cd CALLi
   ```

2. **Configurar el entorno virtual de Python**:
   ```bash
   # Crear entorno virtual
   python -m venv venv

   # Activar el entorno virtual
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate

   # Instalar dependencias
   pip install -r backend-call-automation/requirements.txt
   pip install -e backend-call-automation/
   ```

3. **Configurar variables de entorno**:
   - Copia el archivo `.env.example` a `.env` en el directorio raíz
   - Edita el archivo `.env` con tus configuraciones específicas
   - Para desarrollo local, puedes usar los valores de ejemplo proporcionados

4. **Configurar PYTHONPATH**:
   Para asegurar que las importaciones funcionen correctamente, configura el PYTHONPATH:

   ```bash
   # En Windows (PowerShell):
   $env:PYTHONPATH = "$PWD;$PWD\backend-call-automation"

   # En Windows (CMD):
   set PYTHONPATH=%CD%;%CD%\backend-call-automation

   # En macOS/Linux:
   export PYTHONPATH=$PWD:$PWD/backend-call-automation
   ```

   También puedes usar el script `setup_env.sh` (Linux/macOS) o `setup_env.bat` (Windows) que hemos proporcionado.

5. **Instalar dependencias de frontend**:
   ```bash
   cd frontend-call-automation
   npm install
   ```

## Estructura del Proyecto

```
CALLi/
├── .github/                    # Configuración de GitHub y workflows de CI/CD
├── backend-call-automation/    # Backend de la aplicación
│   ├── app/                    # Código principal de la aplicación
│   │   ├── api/                # Definiciones de API
│   │   ├── config/             # Configuración de la aplicación
│   │   ├── dependencies/       # Dependencias e inyección de dependencias
│   │   ├── middleware/         # Middleware de FastAPI
│   │   ├── models/             # Modelos de datos
│   │   ├── routers/            # Routers de FastAPI
│   │   ├── schemas/            # Esquemas Pydantic
│   │   ├── services/           # Servicios de negocio
│   │   └── utils/              # Utilidades
│   ├── docs/                   # Documentación específica del backend
│   ├── scripts/                # Scripts de utilidad
│   └── tests/                  # Pruebas
├── frontend-call-automation/   # Frontend de la aplicación
├── docs/                       # Documentación general del proyecto
└── scripts/                    # Scripts a nivel de proyecto
```

## Convenciones de Importación

Para mantener la consistencia en el código, seguimos estas convenciones de importación:

1. **Importaciones de dependencias**:
   - Usar `from app.dependencies import ...` para importar dependencias de servicio
   - Las dependencias de configuración deben importarse desde `app.config.dependencies`

2. **Orden de importaciones**:
   - Primero importaciones de la biblioteca estándar
   - Luego importaciones de terceros
   - Finalmente importaciones del proyecto
   - Separar cada grupo con una línea en blanco

3. **Importaciones absolutas vs. relativas**:
   - Preferir importaciones absolutas (ej. `from app.models import User`)
   - Usar importaciones relativas solo para módulos en el mismo paquete

Ejemplo:
```python
# Importaciones de biblioteca estándar
import os
from typing import List, Optional

# Importaciones de terceros
from fastapi import FastAPI, Depends
from pydantic import BaseModel

# Importaciones del proyecto
from app.dependencies import get_db
from app.models.user import User
```

## Ejecución de Pruebas

Para ejecutar las pruebas:

```bash
# Asegúrate de que PYTHONPATH esté configurado correctamente
cd backend-call-automation
python -m pytest tests/
```

Para ejecutar pruebas con cobertura:

```bash
python -m pytest tests/ --cov=app --cov-report=html
```

## Solución de Problemas Comunes

### Error: ModuleNotFoundError

**Problema**: `ModuleNotFoundError: No module named 'app'` o similar.

**Solución**:
1. Verifica que el PYTHONPATH esté configurado correctamente:
   ```bash
   echo $PYTHONPATH  # En Linux/macOS
   echo %PYTHONPATH% # En Windows CMD
   ```
2. Asegúrate de que estás ejecutando los comandos desde el directorio correcto.
3. Si usas un IDE como PyCharm o VS Code, configura el directorio raíz del proyecto como directorio de origen.

### Error: No se pueden encontrar variables de entorno

**Problema**: La aplicación no puede encontrar variables de entorno configuradas.

**Solución**:
1. Verifica que el archivo `.env` exista y tenga los valores correctos.
2. Asegúrate de que estás ejecutando la aplicación desde el directorio correcto.
3. Prueba a cargar manualmente las variables de entorno:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

### Error: Conflictos de dependencias

**Problema**: Errores relacionados con versiones incompatibles de dependencias.

**Solución**:
1. Actualiza todas las dependencias: `pip install --upgrade -r requirements.txt`
2. Si el problema persiste, crea un nuevo entorno virtual y reinstala las dependencias.
3. Verifica si hay conflictos específicos con `pip check`.

## Flujo de Trabajo de Desarrollo

1. **Crear una rama para tu característica o corrección**:
   ```bash
   git checkout -b feature/nombre-de-caracteristica
   ```

2. **Realizar cambios y pruebas**:
   - Implementa tus cambios
   - Escribe pruebas para tus cambios
   - Ejecuta las pruebas para asegurarte de que todo funciona

3. **Enviar cambios**:
   ```bash
   git add .
   git commit -m "Descripción clara de los cambios"
   git push origin feature/nombre-de-caracteristica
   ```

4. **Crear un Pull Request**:
   - Ve a GitHub y crea un PR desde tu rama
   - Describe los cambios realizados
   - Solicita revisión de código

5. **Revisión y Merge**:
   - Aborda los comentarios de la revisión
   - Una vez aprobado, el PR puede ser fusionado
