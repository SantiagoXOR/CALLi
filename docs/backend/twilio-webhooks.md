# Webhooks de Twilio

## Descripción

Los webhooks de Twilio permiten a nuestra aplicación recibir eventos y actualizaciones de estado de las llamadas en tiempo real. Esta documentación detalla la implementación de los endpoints de webhook para Twilio en el Sistema de Automatización de Llamadas.

## Endpoints Implementados

### 1. Webhook Principal (`/api/webhooks/twilio`)

Este endpoint maneja la lógica principal de la llamada y genera respuestas TwiML para controlar el flujo de la conversación.

**Método**: POST

**Respuesta**: TwiML (XML)

**Funcionalidades**:
- Actualiza el estado de la llamada a IN_PROGRESS
- Obtiene información del contacto
- Genera un saludo personalizado
- Reproduce el script de la llamada
- Recopila entrada del usuario (DTMF o voz)
- Maneja el caso de no recibir respuesta

### 2. Webhook de Recopilación (`/api/webhooks/twilio/gather`)

Este endpoint procesa la entrada del usuario durante una llamada y genera respuestas TwiML basadas en dicha entrada.

**Método**: POST

**Respuesta**: TwiML (XML)

**Funcionalidades**:
- Procesa la entrada del usuario (dígitos DTMF o reconocimiento de voz)
- Genera respuestas personalizadas según la entrada
- Actualiza las notas de la llamada con la respuesta del usuario
- Finaliza la llamada de manera adecuada

### 3. Webhook de Estado (`/api/webhooks/twilio/status`)

Este endpoint recibe actualizaciones de estado de las llamadas y actualiza los registros en la base de datos.

**Método**: POST

**Respuesta**: 200 OK

**Funcionalidades**:
- Recibe actualizaciones de estado de Twilio (completed, busy, failed, etc.)
- Actualiza el estado de la llamada en la base de datos
- Registra información adicional (duración, URL de grabación, mensajes de error)
- Actualiza las estadísticas de la campaña cuando la llamada finaliza

## Seguridad

Para garantizar que las solicitudes provienen realmente de Twilio, se implementa un sistema de validación de firmas:

1. Se obtiene la firma de Twilio del encabezado `X-Twilio-Signature`
2. Se construye la URL completa del webhook
3. Se obtienen los parámetros de la solicitud
4. Se valida la firma utilizando el token de autenticación de Twilio

Este proceso de validación se omite en entorno de desarrollo (`APP_DEBUG = True`) para facilitar las pruebas.

## Flujo de Llamada

1. **Inicio de Llamada**:
   - La aplicación inicia una llamada a través del servicio de Twilio
   - Twilio llama al contacto y, cuando responde, envía una solicitud al webhook principal

2. **Interacción con el Usuario**:
   - El webhook principal genera un TwiML con el saludo y el script
   - Se recopila la entrada del usuario (dígitos o voz)
   - La entrada se envía al webhook de recopilación

3. **Procesamiento de Respuesta**:
   - El webhook de recopilación procesa la entrada del usuario
   - Genera una respuesta personalizada
   - Actualiza las notas de la llamada
   - Finaliza la llamada

4. **Finalización de Llamada**:
   - Twilio envía una actualización de estado al webhook de estado
   - La aplicación actualiza el estado de la llamada y las estadísticas de la campaña

## Ejemplos de Respuestas TwiML

### Ejemplo 1: Saludo y Recopilación de Entrada

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="woman" language="es-ES">Hola Juan, le llamamos de Empresa ABC.</Say>
    <Say voice="woman" language="es-ES">Estamos ofreciendo una promoción especial para clientes como usted.</Say>
    <Gather input="dtmf speech" timeout="5" numDigits="1" action="/api/webhooks/twilio/gather" method="POST">
        <Say voice="woman" language="es-ES">Presione 1 si está interesado, 2 si desea que le llamemos más tarde, o diga 'interesado' para recibir más información.</Say>
    </Gather>
    <Say voice="woman" language="es-ES">No hemos recibido respuesta. Gracias por su tiempo, le llamaremos en otro momento.</Say>
    <Hangup/>
</Response>
```

### Ejemplo 2: Respuesta a Usuario Interesado

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="woman" language="es-ES">Gracias por su interés. Un representante se pondrá en contacto con usted pronto para brindarle más información.</Say>
    <Hangup/>
</Response>
```

## Configuración

La configuración de los webhooks se realiza a través de las siguientes variables de entorno:

```dotenv
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
APP_URL=https://your-api.example.com
```

## Consideraciones

1. **Accesibilidad Pública**: Los endpoints de webhook deben ser accesibles públicamente para que Twilio pueda enviar solicitudes.

2. **SSL/TLS**: Se recomienda utilizar HTTPS para garantizar la seguridad de las comunicaciones.

3. **Manejo de Errores**: Los webhooks implementan un manejo robusto de errores para evitar interrupciones en el flujo de la llamada.

4. **Rendimiento**: Los webhooks deben responder rápidamente (< 10 segundos) para evitar tiempos de espera en Twilio.

5. **Monitoreo**: Se recomienda implementar un sistema de monitoreo para detectar problemas en los webhooks.

## Pruebas

Para probar los webhooks localmente, se puede utilizar ngrok para exponer los endpoints locales a Internet:

```bash
ngrok http 8000
```

Luego, se debe configurar la URL de ngrok en la configuración de Twilio:

```dotenv
APP_URL=https://your-ngrok-url.ngrok.io
```
