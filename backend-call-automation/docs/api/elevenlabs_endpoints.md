# ElevenLabs API Integration Endpoints

This document outlines the API endpoints and metrics monitoring for the ElevenLabs integration.

## Implemented Improvements

- **Enhanced Metrics Tracking**:
  - Request duration (total and generation time)
  - Audio quality scoring (basic length validation)
  - Connection pool usage metrics
  - Retry attempt counting
  - Error classification

- **Improved Logging**:
  - Sanitized sensitive parameters
  - Structured log entries
  - Detailed error contexts
  - Performance timing data

## Endpoints

### POST `/api/v1/audio/generate`

Generates audio from text with comprehensive metrics collection.

**Request Body:**

```json
{
  "text": "Texto a convertir en audio.",
  "voice_id": "21m00Tcm4TlvDq8ikWAM", // Optional: Defaults to ELEVENLABS_DEFAULT_VOICE
  "voice_settings": {
    "stability": 0.7,              // Range: 0.0-1.0
    "similarity_boost": 0.75,      // Range: 0.0-1.0
    "style": 0.0,                  // Optional style parameter
    "use_speaker_boost": true      // Recommended for cloned voices
  }
}
```

**Metrics Collected:**
- `elevenlabs_request_duration_seconds` - Total request time
- `elevenlabs_generation_duration_seconds` - Pure synthesis time
- `elevenlabs_audio_quality_score` - Basic quality assessment
- `elevenlabs_pool_usage_ratio` - Connection pool utilization
- `elevenlabs_retry_count_total` - Retry attempts

**Parameters:**

*   `text` (string, required): The text to synthesize.
*   `voice_id` (string, optional): The ElevenLabs voice ID to use. If not provided, the default voice from settings (`ELEVENLABS_DEFAULT_VOICE`) will be used.
*   `voice_settings` (object, optional): Fine-tuning parameters for the voice generation.
    *   `stability` (float, optional): Controls randomness. Higher values are more stable. (Range: 0.0 - 1.0)
    *   `similarity_boost` (float, optional): Boosts similarity to the original voice. (Range: 0.0 - 1.0)
    *   `style` (float, optional): Style exaggeration. (Range might vary, e.g., 0.0 - 1.0)
    *   `use_speaker_boost` (boolean, optional): Recommended for voice cloning.

**Responses:**

*   **`200 OK`**: Successfully generated audio.
    ```json
    {
      "message": "Audio generado exitosamente",
      "audio_id": "unique_audio_identifier_generated", // Optional: ID for reference if stored/cached
      "generation_info": {
         "duration_ms": 2150, // Example duration
         "size_bytes": 180400, // Example size
         "estimated_quality_score": 0.92 // Optional: If quality verification is implemented
      }
    }
    ```
    *   **Note:** The actual audio data might be returned directly in the response body with `Content-Type: audio/mpeg` instead of this JSON structure, depending on API design choices. The JSON response above is an alternative if metadata is returned alongside a link or ID to the audio.

*   **`400 Bad Request`**: Invalid input parameters.
    ```json
    {
      "error_code": "INVALID_INPUT",
      "message": "Entrada inválida.",
      "details": "El campo 'text' no puede estar vacío." // Example detail
    }
    ```
*   **`429 Too Many Requests`**: Rate limit exceeded for the ElevenLabs API key.
    ```json
    {
      "error_code": "RATE_LIMIT_EXCEEDED",
      "message": "Se ha excedido el límite de solicitudes para la API de ElevenLabs.",
      "details": "Reintente después de X segundos." // Detail might include retry info
    }
    ```
*   **`500 Internal Server Error`**: An unexpected error occurred during audio generation.
    ```json
    {
      "error_code": "GENERATION_FAILED",
      "message": "Error interno del servidor durante la generación de audio.",
      "details": "Error específico de la API de ElevenLabs o del servicio." // Example detail
    }
    ```
*   **`503 Service Unavailable`**: The ElevenLabs service is temporarily unavailable or unreachable.
    ```json
    {
      "error_code": "ELEVENLABS_UNAVAILABLE",
      "message": "El servicio de ElevenLabs no está disponible temporalmente.",
      "details": "El servicio retornó un error 503 o no se pudo conectar." // Example detail
    }
    ```

**Notes:**

*   Authentication (e.g., JWT token via Authorization header) is likely required for this endpoint.
*   Consider adding endpoints for listing available voices or managing voice settings if needed.
*   Error responses should follow a consistent format.
