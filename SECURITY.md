# Política de Seguridad

## Versiones Soportadas

Actualmente estamos proporcionando actualizaciones de seguridad para las siguientes versiones:

| Versión | Soportada          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reportar una Vulnerabilidad

Agradecemos los informes de seguridad responsables. Si descubres una vulnerabilidad en CALLi, por favor:

1. **No divulgues públicamente la vulnerabilidad** - No abras un issue público en GitHub.
2. **Envía un correo electrónico** a [santiago@xor.com.ar](mailto:santiago@xor.com.ar) con los detalles de la vulnerabilidad.
3. **Incluye la siguiente información**:
   - Tipo de vulnerabilidad
   - Ruta completa de los archivos afectados
   - Ubicación del código fuente relacionado
   - Cualquier solución potencial que hayas identificado

## Proceso de Respuesta

Cuando recibamos un informe de vulnerabilidad, seguiremos estos pasos:

1. Confirmaremos la recepción del informe dentro de las 48 horas.
2. Proporcionaremos una estimación de cuándo podemos esperar tener una resolución.
3. Verificaremos la vulnerabilidad y determinaremos su impacto.
4. Desarrollaremos y probaremos una solución.
5. Lanzaremos una actualización que aborde la vulnerabilidad.
6. Reconoceremos públicamente tu contribución (si lo deseas) después de resolver el problema.

## Prácticas de Seguridad

El proyecto CALLi implementa las siguientes prácticas de seguridad:

- Análisis regular de dependencias para detectar vulnerabilidades
- Escaneo de código para identificar problemas de seguridad
- Revisión de código por pares para todas las contribuciones
- Pruebas automatizadas para prevenir regresiones de seguridad
- Cifrado de datos sensibles en reposo y en tránsito
- Autenticación y autorización adecuadas para todos los endpoints
- Principio de mínimo privilegio en todos los flujos de trabajo
- Enmascaramiento seguro de información sensible en logs y salidas

### Manejo de Secretos

#### Qué NO hacer

- ❌ **NO** incluir secretos, contraseñas o tokens en el código fuente
- ❌ **NO** almacenar secretos en archivos de configuración sin cifrar
- ❌ **NO** registrar secretos en logs o salidas de consola
- ❌ **NO** compartir secretos a través de canales no seguros (correo electrónico, mensajería, etc.)

#### Qué hacer

- ✅ Usar variables de entorno para secretos en entornos de desarrollo y producción
- ✅ Utilizar servicios de gestión de secretos como AWS Secrets Manager, HashiCorp Vault, etc.
- ✅ Rotar secretos regularmente
- ✅ Usar diferentes secretos para diferentes entornos (desarrollo, pruebas, producción)

### Enmascaramiento de Información Sensible

Al registrar información que podría contener datos sensibles:

1. **Enmascarar completamente** los valores sensibles sin mostrar ninguna parte del original
2. Usar la función `secure_mask_secret` del módulo `improved_security_utils.py`
3. Proporcionar información de contexto sin revelar el contenido real

Ejemplo:

```python
# Incorrecto
logger.info(f"API Key: {api_key[:4]}****")

# Correcto
from scripts.improved_security_utils import secure_mask_secret
logger.info(f"API Key: {secure_mask_secret(api_key)}")
```

### Manejo de Excepciones

Para un manejo seguro de excepciones:

1. Usar `logger.exception()` en lugar de `logger.error()` para capturar el stack trace completo
2. Usar `raise ... from e` para preservar el contexto de la excepción
3. No exponer detalles de implementación en mensajes de error mostrados al usuario

Ejemplo:

```python
try:
    # Código que puede fallar
except SomeException as e:
    logger.exception(f"Error al procesar la solicitud: {e}")
    raise CustomException("Mensaje genérico para el usuario") from e
```

### Verificación de Seguridad con Pre-commit

Usar pre-commit para verificar problemas de seguridad antes de confirmar cambios:

```bash
# Instalar dependencias
python scripts/install_precommit_deps.py

# Ejecutar verificaciones
pre-commit run --all-files
```

### Verificación de Seguridad Local

El proyecto incluye un script de verificación de seguridad local que puede ejecutarse en cualquier momento para identificar problemas de seguridad:

```bash
# Ejecutar verificación de seguridad local
python scripts/security_check_local.py
```

Este script realiza las siguientes verificaciones:

- Presencia de archivos de seguridad requeridos
- Encabezados de seguridad en la configuración de nginx
- Dependencias de Python con vulnerabilidades conocidas
- Dependencias de JavaScript con vulnerabilidades conocidas
- Secretos en el código fuente

#### Configuración de la Verificación de Seguridad

Para personalizar la verificación de seguridad, puedes modificar el archivo `scripts/security_check_config.json`:

```json
{
    "exclude_dirs": [
        ".git",
        "node_modules",
        ".venv",
        "venv",
        "__pycache__",
        "dist",
        "build"
    ],
    "exclude_files": [
        ".env.example",
        "security_check.py",
        "security_check_local.py"
    ],
    "exclude_patterns": [
        "http://[^\"']+",
        "https://[^\"']+"
    ]
}
```

Esta configuración permite excluir directorios, archivos y patrones específicos de la búsqueda de secretos, reduciendo los falsos positivos.

## Reconocimientos

Queremos agradecer a las siguientes personas que han contribuido a mejorar la seguridad de CALLi:

- Lista de contribuyentes (se actualizará cuando corresponda)
