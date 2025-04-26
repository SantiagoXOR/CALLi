# Documentación Técnica: Sistema de Caché de Audio

## Introducción

El Sistema de Caché de Audio es una solución implementada para optimizar el rendimiento y reducir costos en la generación de audio mediante la API de ElevenLabs. Este documento describe la arquitectura, funcionamiento y consideraciones técnicas de esta implementación.

## Arquitectura

### Componentes Principales

1. **AudioCacheService**: Servicio principal que gestiona todas las operaciones de caché.
2. **Sistema de Almacenamiento**: Utiliza el sistema de archivos para almacenar los archivos de audio.
3. **Sistema de Metadatos**: Gestiona información sobre los archivos almacenados en caché.
4. **Integración con ElevenLabsService**: Modificación del servicio existente para utilizar el caché.
5. **API de Gestión**: Endpoints para monitorear y administrar el caché.

### Diagrama de Flujo

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Cliente     │────▶│ API Backend │────▶│ ElevenLabs  │
└─────────────┘     └──────┬──────┘     └─────────────┘
                          │                    ▲
                          ▼                    │
                    ┌─────────────┐     ┌─────────────┐
                    │ AudioCache  │────▶│ Sistema de  │
                    │ Service     │     │ Archivos    │
                    └─────────────┘     └─────────────┘
```

## Implementación

### Configuración

El sistema de caché se configura mediante las siguientes variables en `settings.py`:

```python
# Audio Cache Configuration
AUDIO_CACHE_ENABLED: bool = True
AUDIO_CACHE_DIR: str = "cache/audio"
AUDIO_CACHE_TTL: int = 86400  # 24 horas en segundos
AUDIO_CACHE_MAX_SIZE: int = 1073741824  # 1 GB en bytes
```

### Generación de Claves de Caché

Para identificar de manera única cada archivo de audio, se utiliza un hash MD5 basado en:
- El texto a convertir (normalizado)
- El ID de la voz utilizada
- El idioma del texto

```python
def _generate_cache_key(self, text: str, voice_id: str, language: str = "es") -> str:
    # Normalizar texto (eliminar espacios extra, convertir a minúsculas)
    normalized_text = " ".join(text.lower().split())
    
    # Crear hash del texto + voz + idioma
    hash_input = f"{normalized_text}|{voice_id}|{language}"
    hash_value = hashlib.md5(hash_input.encode()).hexdigest()
    
    return hash_value
```

### Flujo de Operación

1. **Búsqueda en Caché**:
   - Al solicitar audio, primero se verifica si existe en el caché.
   - Si existe y no ha expirado, se devuelve directamente.

2. **Generación y Almacenamiento**:
   - Si no existe en caché, se genera mediante la API de ElevenLabs.
   - El audio generado se almacena en el sistema de archivos.
   - Se actualizan los metadatos con información sobre el archivo.

3. **Limpieza Automática**:
   - Cuando el caché alcanza su tamaño máximo, se eliminan los archivos menos utilizados.
   - Los archivos se ordenan por fecha de último acceso y frecuencia de uso.

4. **Invalidación**:
   - Los archivos expiran después del TTL configurado.
   - Se pueden invalidar manualmente a través de la API.

### Metadatos

Para cada archivo en caché, se almacena la siguiente información:

```json
{
  "path": "/path/to/file.mp3",
  "size": 123456,
  "created_at": "2023-04-25T18:30:00.000Z",
  "last_accessed": "2023-04-25T19:45:00.000Z",
  "access_count": 5,
  "text": "Texto original (truncado si es muy largo)...",
  "voice_id": "voice_id",
  "language": "es"
}
```

## Integración con ElevenLabsService

El servicio `ElevenLabsService` se modificó para utilizar el caché:

1. Se añadió un parámetro `language` al método `generate_stream`.
2. Se implementó la verificación de caché antes de llamar a la API.
3. Se añadió la recolección de chunks para guardar en caché.

```python
async def generate_stream(self, text: str, voice_id: str = "default_voice", language: str = "es") -> AsyncGenerator[bytes, None]:
    # Verificar si el audio está en caché
    cached_file_path = await audio_cache_service.get_from_cache(text, voice_id, language)
    if cached_file_path:
        # Devolver desde caché
        # ...
    
    # Si no está en caché, generar desde la API
    # ...
    
    # Guardar en caché
    audio_data = b''.join(all_chunks)
    asyncio.create_task(
        audio_cache_service.save_to_cache(text, voice_id, audio_data, language)
    )
```

## API de Gestión

Se implementaron los siguientes endpoints para gestionar el caché:

1. **GET /api/audio-cache/stats**: Obtiene estadísticas del caché.
2. **POST /api/audio-cache/clear**: Limpia todo el caché.

## Consideraciones de Rendimiento

### Ventajas

1. **Reducción de Latencia**: Los audios frecuentes se sirven directamente desde el disco local.
2. **Ahorro de Costos**: Se reducen las llamadas a la API de ElevenLabs.
3. **Resiliencia**: El sistema puede seguir funcionando parcialmente si la API externa no está disponible.

### Consideraciones

1. **Uso de Disco**: El caché puede crecer significativamente con el tiempo.
2. **Consistencia**: Si cambia la voz o el modelo en ElevenLabs, el caché puede contener versiones antiguas.
3. **Concurrencia**: El sistema maneja múltiples solicitudes simultáneas de manera segura.

## Métricas y Monitoreo

El sistema proporciona las siguientes métricas para monitoreo:

1. **Tamaño Total**: Espacio total utilizado por el caché.
2. **Tasa de Aciertos**: Porcentaje de solicitudes servidas desde el caché.
3. **Distribución por Voz**: Uso del caché por cada voz.
4. **Archivos Más Accedidos**: Lista de los archivos más utilizados.

## Seguridad

1. **Validación de Entrada**: Se normalizan y validan todos los textos antes de generar claves de caché.
2. **Límites de Tamaño**: Se establecen límites para evitar ataques de denegación de servicio.
3. **Aislamiento**: El caché opera en un directorio específico y aislado.

## Conclusiones

El Sistema de Caché de Audio proporciona una solución eficiente para optimizar el rendimiento y reducir costos en la generación de audio. Su diseño modular y configurable permite adaptarse a diferentes necesidades y escalas de uso.

## Referencias

- [Documentación de ElevenLabs API](https://docs.elevenlabs.io/api-reference)
- [Estrategias de Caché](https://codeahoy.com/2017/08/11/caching-strategies-and-how-to-choose-the-right-one/)
- [Optimización de Almacenamiento de Audio](https://developers.google.com/web/fundamentals/media/recording-audio)
