AIConversationService
====================

Descripción
----------
Servicio principal para el procesamiento de conversaciones usando IA.

Componentes Principales
--------------------
- Procesador de Mensajes
- Gestor de Memoria de Conversación
- Analizador de Sentimientos
- Sistema de Sugerencias de Acciones

Integración con LangChain
-----------------------
El servicio utiliza LangChain para:
- Gestión de cadenas de conversación
- Memoria de buffer
- Plantillas de prompts personalizables
- Integración con OpenAI GPT-4

Ejemplos de Uso
-------------
.. code-block:: python

    ai_service = AIConversationService(model_name="gpt-4")
    response = await ai_service.process_message(
        message="¿Qué beneficios tiene este producto?",
        context={"campaign_type": "sales"},
        conversation_id="conv_123"
    )
