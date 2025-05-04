# Guía de Solución de Problemas

Esta guía proporciona soluciones para problemas comunes que pueden surgir durante el desarrollo y ejecución del proyecto CALLi.

## Problemas de Entorno y Configuración

### Error: ModuleNotFoundError

**Problema**:
```
ModuleNotFoundError: No module named 'app.dependencies'
```

**Causas posibles**:
- PYTHONPATH no configurado correctamente
- Estructura de directorios incorrecta
- Archivo `__init__.py` faltante en algún directorio

**Soluciones**:

1. **Verificar PYTHONPATH**:
   ```bash
   # En Linux/macOS
   echo $PYTHONPATH

   # En Windows (CMD)
   echo %PYTHONPATH%

   # En Windows (PowerShell)
   echo $env:PYTHONPATH
   ```

   El PYTHONPATH debe incluir tanto el directorio raíz del proyecto como el directorio `backend-call-automation`.

2. **Configurar PYTHONPATH**:
   ```bash
   # En Linux/macOS
   export PYTHONPATH=$PWD:$PWD/backend-call-automation

   # En Windows (CMD)
   set PYTHONPATH=%CD%;%CD%\backend-call-automation

   # En Windows (PowerShell)
   $env:PYTHONPATH = "$PWD;$PWD\backend-call-automation"
   ```

3. **Verificar archivos `__init__.py`**:
   Asegúrate de que cada directorio en la ruta de importación tenga un archivo `__init__.py`.

   ```bash
   # Verificar la existencia de __init__.py en directorios clave
   ls -la backend-call-automation/app/__init__.py
   ls -la backend-call-automation/app/dependencies/__init__.py
   ```

4. **Instalar el paquete en modo desarrollo**:
   ```bash
   pip install -e backend-call-automation/
   ```

### Error: Variables de Entorno No Encontradas

**Problema**:
```
KeyError: 'SUPABASE_URL'
```

**Causas posibles**:
- Archivo `.env` faltante o incompleto
- Variables de entorno no cargadas
- Ejecución desde un directorio incorrecto

**Soluciones**:

1. **Verificar archivo `.env`**:
   ```bash
   # Verificar existencia del archivo .env
   ls -la .env

   # Verificar contenido
   cat .env | grep SUPABASE_URL
   ```

2. **Crear archivo `.env` desde la plantilla**:
   ```bash
   cp .env.example .env
   # Editar .env con los valores correctos
   ```

3. **Cargar manualmente las variables de entorno**:
   ```python
   from dotenv import load_dotenv
   import os

   # Cargar desde un archivo específico
   load_dotenv('/ruta/completa/a/.env')

   # Verificar que se haya cargado
   print(os.environ.get('SUPABASE_URL', 'No encontrado'))
   ```

## Problemas de Dependencias

### Error: Conflictos de Versiones

**Problema**:
```
ImportError: cannot import name 'X' from 'Y'
```

**Causas posibles**:
- Versiones incompatibles de paquetes
- Dependencias faltantes
- Conflictos entre paquetes

**Soluciones**:

1. **Verificar versiones instaladas**:
   ```bash
   pip list | grep nombre-del-paquete
   ```

2. **Actualizar dependencias**:
   ```bash
   pip install --upgrade -r backend-call-automation/requirements.txt
   ```

3. **Crear un nuevo entorno virtual**:
   ```bash
   # Eliminar el entorno virtual actual
   deactivate
   rm -rf venv

   # Crear un nuevo entorno virtual
   python -m venv venv
   source venv/bin/activate  # En Linux/macOS
   venv\Scripts\activate     # En Windows

   # Instalar dependencias
   pip install -r backend-call-automation/requirements.txt
   ```

4. **Verificar conflictos**:
   ```bash
   pip check
   ```

## Problemas de Ejecución

### Error: Conexión a Supabase

**Problema**:
```
supabase._sync.client.SupabaseException: Invalid URL
```

**Causas posibles**:
- URL de Supabase incorrecta
- Clave de API de Supabase incorrecta
- Problemas de red

**Soluciones**:

1. **Verificar configuración de Supabase**:
   ```bash
   # Verificar variables de entorno
   echo $SUPABASE_URL
   echo $SUPABASE_KEY
   ```

2. **Probar conexión a Supabase**:
   ```python
   from supabase import create_client

   url = "tu-url-de-supabase"
   key = "tu-clave-de-supabase"

   try:
       supabase = create_client(url, key)
       # Intentar una operación simple
       result = supabase.table('test').select('*').execute()
       print("Conexión exitosa")
   except Exception as e:
       print(f"Error de conexión: {e}")
   ```

3. **Verificar acceso a internet y firewall**:
   ```bash
   # Verificar conectividad
   ping supabase.co
   ```

### Error: Problemas con Twilio

**Problema**:
```
twilio.base.exceptions.TwilioRestException: HTTP 401 error
```

**Causas posibles**:
- Credenciales de Twilio incorrectas
- Número de teléfono no verificado
- Cuenta de Twilio sin fondos

**Soluciones**:

1. **Verificar credenciales de Twilio**:
   ```bash
   # Verificar variables de entorno
   echo $TWILIO_ACCOUNT_SID
   echo $TWILIO_AUTH_TOKEN
   ```

2. **Probar conexión a Twilio**:
   ```python
   from twilio.rest import Client

   account_sid = 'tu-account-sid'
   auth_token = 'tu-auth-token'

   try:
       client = Client(account_sid, auth_token)
       # Intentar una operación simple
       account = client.api.accounts(account_sid).fetch()
       print(f"Conexión exitosa: {account.friendly_name}")
   except Exception as e:
       print(f"Error de conexión: {e}")
   ```

3. **Verificar estado de la cuenta de Twilio**:
   Visita el [Panel de Twilio](https://www.twilio.com/console) para verificar el estado de tu cuenta.

## Problemas de Pruebas

### Error: Pruebas Fallando

**Problema**:
```
FAILED tests/test_services/test_call_service.py::test_make_call
```

**Causas posibles**:
- Configuración de prueba incorrecta
- Mocks o fixtures faltantes
- Cambios en el código que rompen las pruebas

**Soluciones**:

1. **Ejecutar prueba específica con más detalles**:
   ```bash
   python -m pytest tests/test_services/test_call_service.py::test_make_call -v
   ```

2. **Verificar configuración de prueba**:
   ```bash
   # Verificar conftest.py
   cat tests/conftest.py
   ```

3. **Actualizar mocks y fixtures**:
   Asegúrate de que los mocks y fixtures estén actualizados con los cambios recientes en el código.

4. **Depurar con pdb**:
   ```bash
   python -m pytest tests/test_services/test_call_service.py::test_make_call --pdb
   ```

### Error: Cobertura de Pruebas Baja

**Problema**:
```
TOTAL                                                           3144     1021    68%
```

**Causas posibles**:
- Pruebas insuficientes
- Código no probado
- Configuración de cobertura incorrecta

**Soluciones**:

1. **Generar informe de cobertura detallado**:
   ```bash
   python -m pytest --cov=app --cov-report=html
   ```

2. **Identificar áreas con baja cobertura**:
   Abre el informe HTML generado y busca áreas con baja cobertura.

3. **Agregar pruebas para áreas con baja cobertura**:
   Prioriza la adición de pruebas para la lógica de negocio crítica.

## Problemas de CI/CD

### Error: Workflow de GitHub Actions Fallando

**Problema**:
```
Error: Process completed with exit code 1.
```

**Causas posibles**:
- Pruebas fallando
- Dependencias faltantes
- Configuración de CI incorrecta

**Soluciones**:

1. **Revisar logs de GitHub Actions**:
   Ve a la pestaña "Actions" en GitHub y revisa los logs detallados del workflow fallido.

2. **Verificar configuración de workflow**:
   ```bash
   cat .github/workflows/nombre-del-workflow.yml
   ```

3. **Ejecutar pruebas localmente**:
   ```bash
   # Ejecutar las mismas pruebas que se ejecutan en CI
   python -m pytest
   ```

4. **Verificar dependencias**:
   Asegúrate de que todas las dependencias estén especificadas en `requirements.txt`.

## Problemas de Rendimiento

### Error: Tiempos de Respuesta Lentos

**Problema**: La API responde lentamente o se agota el tiempo de espera.

**Causas posibles**:
- Consultas de base de datos ineficientes
- Servicios externos lentos
- Recursos insuficientes

**Soluciones**:

1. **Identificar cuellos de botella**:
   ```python
   import time

   start_time = time.time()
   # Operación a medir
   end_time = time.time()
   print(f"Tiempo de ejecución: {end_time - start_time} segundos")
   ```

2. **Optimizar consultas de base de datos**:
   - Agregar índices
   - Limitar resultados
   - Usar consultas más eficientes

3. **Implementar caché**:
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=128)
   def get_data(key):
       # Operación costosa
       return result
   ```

4. **Monitorear servicios externos**:
   Implementa métricas y alertas para servicios externos.

## Recursos Adicionales

- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de Supabase](https://supabase.io/docs)
- [Documentación de Twilio](https://www.twilio.com/docs)
- [Documentación de pytest](https://docs.pytest.org/)
- [Guía de GitHub Actions](https://docs.github.com/en/actions)
