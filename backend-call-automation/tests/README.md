# Tests del Sistema de Automatización de Llamadas

## Estructura de Tests
- `test_routers/`: Tests de endpoints HTTP
- `test_services/`: Tests de lógica de negocio
- `test_models/`: Tests de modelos y validaciones
- `test_config/`: Tests de configuración del sistema

## Tests de Configuración
Los tests de configuración verifican que todas las variables de entorno necesarias estén presentes y tengan el formato correcto:

- `test_settings_loaded`: Verifica la carga básica de configuración (nombre de la aplicación, entorno y modo de depuración)
- `test_database_config`: Valida la configuración de la base de datos (URL de conexión)
- `test_supabase_config`: Comprueba la configuración de Supabase (URL, clave de API y clave de servicio)
- `test_twilio_config`: Verifica la configuración de Twilio (SID de cuenta, token de autenticación y número de teléfono)
- `test_redis_client`: Verifica la funcionalidad del cliente Redis (generación de claves, operaciones de caché y manejo de expiración)

## Fixtures Disponibles
- `async_client`: Cliente HTTP para tests de endpoints
- `mock_campaign_data`: Datos de ejemplo para campañas
- `mock_supabase_client`: Mock del cliente Supabase
- `mock_twilio_client`: Mock del cliente Twilio

## Tests de Routers

### Endpoints de Campañas

#### Crear Campaña
- **Endpoint**: `POST /api/campaigns/`
- **Descripción**: Crea una nueva campaña.
- **Request**:
  ```json
  {
    "name": "Test Campaign",
    "description": "This is a test campaign"
  }
  ```
- **Response**:
  ```json
  {
    "id": "1",
    "name": "Test Campaign",
    "description": "This is a test campaign",
    "created_at": "2023-10-01T12:00:00Z"
  }
  ```

#### Obtener Campaña
- **Endpoint**: `GET /api/campaigns/{campaign_id}`
- **Descripción**: Obtiene una campaña por su ID.
- **Request**: N/A
- **Response**:
  ```json
  {
    "id": "1",
    "name": "Test Campaign",
    "description": "This is a test campaign",
    "created_at": "2023-10-01T12:00:00Z"
  }
  ```

#### Listar Campañas
- **Endpoint**: `GET /api/campaigns/`
- **Descripción**: Lista todas las campañas con paginación.
- **Request**: N/A
- **Response**:
  ```json
  [
    {
      "id": "1",
      "name": "Test Campaign",
      "description": "This is a test campaign",
      "created_at": "2023-10-01T12:00:00Z"
    }
  ]
  ```

#### Actualizar Campaña
- **Endpoint**: `PATCH /api/campaigns/{campaign_id}`
- **Descripción**: Actualiza una campaña existente.
- **Request**:
  ```json
  {
    "name": "Updated Campaign",
    "description": "This is an updated campaign"
  }
  ```
- **Response**:
  ```json
  {
    "id": "1",
    "name": "Updated Campaign",
    "description": "This is an updated campaign",
    "created_at": "2023-10-01T12:00:00Z"
  }
  ```

#### Eliminar Campaña
- **Endpoint**: `DELETE /api/campaigns/{campaign_id}`
- **Descripción**: Elimina una campaña por su ID.
- **Request**: N/A
- **Response**:
  ```json
  true
  ```

#### Actualizar Estadísticas de Campaña
- **Endpoint**: `PATCH /api/campaigns/{campaign_id}/stats`
- **Descripción**: Actualiza las estadísticas de una campaña.
- **Request**:
  ```json
  {
    "total_calls": 100,
    "successful_calls": 80,
    "failed_calls": 10,
    "pending_calls": 10
  }
  ```
- **Response**:
  ```json
  {
    "id": "1",
    "name": "Test Campaign",
    "description": "This is a test campaign",
    "total_calls": 100,
    "successful_calls": 80,
    "failed_calls": 10,
    "pending_calls": 10,
    "created_at": "2023-10-01T12:00:00Z"
  }
  ```
## Ejecución de Tests
```bash
# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar tests específicos
pytest tests/test_routers/test_campaign_router.py -v
pytest tests/test_services/test_campaign_service.py -v
pytest tests/test_config/test_settings.py -v
```

## Documentación de Código
Cada módulo y función de prueba incluye documentación detallada mediante docstrings que explica:

1. El propósito general del módulo de pruebas
2. La funcionalidad específica que cada prueba verifica
3. Los parámetros que se prueban y sus valores esperados
4. Las condiciones de éxito para cada prueba

Ejemplo de documentación de una función de prueba:
```python
def test_settings_loaded():
    """
    Verifica que la configuración básica de la aplicación se cargue correctamente.

    Esta prueba asegura que los parámetros fundamentales de la aplicación como
    el nombre, el entorno y el modo de depuración tengan los valores esperados
    durante la ejecución de pruebas.
    """
```

## Convenciones de Testing
1. Usar nombres descriptivos para los tests
2. Seguir el patrón AAA (Arrange, Act, Assert)
3. Mantener los tests independientes
4. Usar fixtures para código reutilizable
5. Documentar casos especiales o complejos
6. Incluir docstrings detallados en cada módulo y función de prueba
