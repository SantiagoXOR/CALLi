"""
Servicio mejorado para manejar conversaciones con IA usando LangChain.
Este servicio proporciona funcionalidades avanzadas para generar respuestas
personalizadas según el tipo de campaña y el contexto de la conversación.
"""

import asyncio
import json
import logging
from typing import Any

from fastapi import HTTPException
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from app.config.ai_config import AISettings

logger = logging.getLogger(__name__)
settings = AISettings()


class EnhancedAIConversationService:
    """
    Servicio mejorado para manejar conversaciones con IA.

    Este servicio proporciona funcionalidades avanzadas para generar respuestas
    personalizadas según el tipo de campaña y el contexto de la conversación.
    """

    def __init__(self) -> None:
        """Inicializa el servicio de conversación con IA."""
        self.settings = settings
        self.llm = self._initialize_llm()
        self._rate_limit_semaphore = asyncio.Semaphore(5)
        self.prompt_templates = self._load_prompt_templates()

    def _initialize_llm(self) -> Any:
        """
        Inicializa el modelo de lenguaje según la configuración.

        Returns:
            Instancia del modelo de lenguaje (OpenAI o Google)
        """
        if self.settings.LLM_PROVIDER == "openai":
            return ChatOpenAI(
                model_name=self.settings.DEFAULT_MODEL,
                temperature=self.settings.TEMPERATURE,
                max_tokens=self.settings.MAX_TOKENS,
                api_key=self.settings.OPENAI_API_KEY,
            )
        if self.settings.LLM_PROVIDER == "google":
            return ChatGoogleGenerativeAI(
                model=self.settings.GOOGLE_MODEL,
                temperature=self.settings.TEMPERATURE,
                max_output_tokens=self.settings.MAX_TOKENS,
                google_api_key=self.settings.GOOGLE_API_KEY,
                convert_system_message_to_human=True,
            )
        raise ValueError(f"Proveedor de LLM no soportado: {self.settings.LLM_PROVIDER}")

    def _load_prompt_templates(self) -> dict[str, PromptTemplate]:
        """
        Carga las plantillas de prompts para diferentes tipos de campaña.

        Returns:
            Dict[str, PromptTemplate]: Diccionario de plantillas de prompts
        """
        prompt_templates = {}

        for campaign_type, template_str in self.settings.CAMPAIGN_PROMPTS.items():
            prompt_templates[campaign_type] = PromptTemplate(
                input_variables=self.settings.REQUIRED_VARIABLES[campaign_type],
                template=template_str,
            )

        return prompt_templates

    async def process_message(
        self,
        message: str,
        campaign_type: str = "sales",
        conversation_id: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Procesa un mensaje y genera una respuesta personalizada según el tipo de campaña.

        Args:
            message: Mensaje del usuario
            campaign_type: Tipo de campaña (sales, support, survey, etc.)
            conversation_id: ID de la conversación (opcional)
            context: Contexto adicional para la conversación (opcional)

        Returns:
            Dict con la respuesta y metadatos
        """
        async with self._rate_limit_semaphore:
            try:
                # Validar tipo de campaña
                if campaign_type not in self.prompt_templates:
                    logger.warning(
                        f"Tipo de campaña no soportado: {campaign_type}, usando 'sales' por defecto"
                    )
                    campaign_type = "sales"

                # Inicializar contexto si es None
                context = context or {}

                # 1. Recuperar historial de caché
                history = await self._get_conversation_history(conversation_id)

                # 2. Preparar variables para el prompt
                prompt_variables = self._prepare_prompt_variables(
                    campaign_type, message, history, context
                )

                # 3. Generar respuesta
                response = await self._generate_response(campaign_type, prompt_variables)

                # 4. Actualizar historial de conversación
                await self._update_conversation_history(conversation_id, message, response)

                # 5. Analizar sentimiento
                input_sentiment = await self.analyze_sentiment(message)
                response_sentiment = await self.analyze_sentiment(response)

                # 6. Sugerir acciones
                suggested_actions = await self.suggest_actions(
                    message, response, input_sentiment, context
                )

                # 7. Guardar métricas
                if conversation_id:
                    await self._save_conversation_metrics(
                        conversation_id,
                        message,
                        response,
                        input_sentiment,
                        response_sentiment,
                        campaign_type,
                    )

                return {
                    "response": response,
                    "input_sentiment": input_sentiment,
                    "response_sentiment": response_sentiment,
                    "suggested_actions": suggested_actions,
                    "conversation_id": conversation_id,
                    "campaign_type": campaign_type,
                }

            except Exception as e:
                logger.error(f"Error al procesar mensaje: {e!s}")
                raise HTTPException(status_code=500, detail=f"Error al procesar mensaje: {e!s}")

    async def _get_conversation_history(self, conversation_id: str | None) -> str:
        """
        Recupera el historial de conversación desde la caché.

        Args:
            conversation_id: ID de la conversación

        Returns:
            Historial de conversación formateado
        """
        if not conversation_id:
            return ""

        try:
            # Implementar lógica para recuperar historial desde Redis o base de datos
            # Por ahora, retornamos un string vacío
            return ""
        except Exception as e:
            logger.error(f"Error al recuperar historial de conversación: {e!s}")
            return ""

    def _prepare_prompt_variables(
        self, campaign_type: str, message: str, history: str, context: dict[str, Any]
    ) -> dict[str, str]:
        """
        Prepara las variables para el prompt según el tipo de campaña.

        Args:
            campaign_type: Tipo de campaña
            message: Mensaje del usuario
            history: Historial de conversación
            context: Contexto adicional

        Returns:
            Dict con las variables para el prompt
        """
        # Obtener las variables requeridas para este tipo de campaña
        required_vars = self.settings.REQUIRED_VARIABLES[campaign_type]

        # Inicializar con valores por defecto
        variables = {"history": history, "input": message}

        # Añadir valores del contexto
        for var in required_vars:
            if var in context:
                variables[var] = context[var]
            elif var in self.settings.DEFAULT_VALUES:
                variables[var] = self.settings.DEFAULT_VALUES[var]
            elif var not in variables:
                # Si es una variable requerida y no está en el contexto ni en los valores por defecto
                logger.warning(
                    f"Variable requerida '{var}' no proporcionada para prompt de tipo '{campaign_type}'"
                )
                variables[var] = f"[{var} no proporcionado]"

        return variables

    async def _generate_response(self, campaign_type: str, variables: dict[str, str]) -> str:
        """
        Genera una respuesta utilizando el modelo de lenguaje.

        Args:
            campaign_type: Tipo de campaña
            variables: Variables para el prompt

        Returns:
            Respuesta generada
        """
        try:
            prompt_template = self.prompt_templates[campaign_type]
            prompt = prompt_template.format(**variables)

            # Generar respuesta
            response = await self.llm.ainvoke(prompt)

            return response
        except Exception as e:
            logger.error(f"Error al generar respuesta: {e!s}")
            return "Lo siento, no pude generar una respuesta en este momento. Por favor, inténtelo de nuevo más tarde."

    async def _update_conversation_history(
        self, conversation_id: str | None, message: str, response: str
    ) -> None:
        """
        Actualiza el historial de conversación en la caché.

        Args:
            conversation_id: ID de la conversación
            message: Mensaje del usuario
            response: Respuesta generada
        """
        if not conversation_id:
            return

        try:
            # Implementar lógica para actualizar historial en Redis o base de datos
            pass
        except Exception as e:
            logger.error(f"Error al actualizar historial de conversación: {e!s}")

    async def analyze_sentiment(self, text: str) -> dict[str, Any]:
        """
        Analiza el sentimiento del texto.

        Args:
            text: Texto a analizar

        Returns:
            Dict con análisis de sentimiento
        """
        output_parser = JsonOutputParser()
        prompt = PromptTemplate(
            input_variables=["text"],
            partial_variables={"format_instructions": output_parser.get_format_instructions()},
            template="""Analiza el sentimiento del siguiente texto y clasifícalo.
            Texto: {text}
            Devuelve un objeto JSON con la emoción primaria (primary_emotion) y su puntuación (score). \n{format_instructions}""",
        )

        try:
            response = await self.llm.ainvoke(prompt.format(text=text))
            return json.loads(response)
        except Exception as e:
            logger.error(f"Error al analizar el sentimiento: {e}")
            return {"primary_emotion": "neutral", "score": 0.5}

    async def suggest_actions(
        self,
        message: str,
        response: str,
        sentiment: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> list[dict[str, str]]:
        """
        Sugiere acciones basadas en el mensaje, la respuesta y el sentimiento.

        Args:
            message: Mensaje del usuario
            response: Respuesta generada
            sentiment: Análisis de sentimiento
            context: Contexto adicional

        Returns:
            Lista de acciones sugeridas
        """
        try:
            output_parser = JsonOutputParser()
            prompt = PromptTemplate(
                input_variables=["message", "response", "sentiment", "context"],
                partial_variables={"format_instructions": output_parser.get_format_instructions()},
                template="""
                Basándote en la siguiente interacción, sugiere hasta 3 acciones a tomar:

                Mensaje del usuario: {message}

                Respuesta del sistema: {response}

                Análisis de sentimiento: {sentiment}

                Contexto adicional: {context}

                Proporciona hasta 3 acciones recomendadas en formato JSON:
                [
                    {{
                        "action_type": "continue_conversation/offer_callback/escalate/end_conversation/send_information",
                        "priority": "high/medium/low",
                        "description": "descripción de la acción",
                        "reason": "razón para esta acción"
                    }}
                ]
                \n{format_instructions}
                """,
            )

            response = await self.llm.ainvoke(
                prompt.format(
                    message=message,
                    response=response,
                    sentiment=json.dumps(sentiment),
                    context=json.dumps(context or {}),
                )
            )

            return json.loads(response)
        except Exception as e:
            logger.error(f"Error al sugerir acciones: {e!s}")
            return [
                {
                    "action_type": "continue_conversation",
                    "priority": "medium",
                    "description": "Continuar la conversación normalmente",
                    "reason": "Error al generar sugerencias personalizadas",
                }
            ]

    async def _save_conversation_metrics(
        self,
        conversation_id: str,
        message: str,
        response: str,
        input_sentiment: dict[str, Any],
        response_sentiment: dict[str, Any],
        campaign_type: str,
    ) -> None:
        """
        Guarda métricas de la conversación para análisis posterior.

        Args:
            conversation_id: ID de la conversación
            message: Mensaje del usuario
            response: Respuesta generada
            input_sentiment: Análisis de sentimiento del mensaje
            response_sentiment: Análisis de sentimiento de la respuesta
            campaign_type: Tipo de campaña
        """
        try:
            # Implementar lógica para guardar métricas en base de datos
            pass
        except Exception as e:
            logger.error(f"Error al guardar métricas de conversación: {e!s}")
