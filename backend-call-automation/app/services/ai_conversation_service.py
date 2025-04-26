"""Servicio para manejar conversaciones con IA usando LangChain."""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from fastapi import HTTPException
import asyncio
import logging
import json
from datetime import datetime
from typing import Any

from app.config.ai_config import AISettings
from app.config.supabase import supabase_client
from app.config.redis_client import generate_conversation_cache_key

logger = logging.getLogger(__name__)
settings = AISettings()

class AIConversationService:
    def __init__(self, model_name: str = "gpt-4"):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=settings.GOOGLE_API_KEY,
            convert_system_message_to_human=True
        )
        self._rate_limit_semaphore = asyncio.Semaphore(5)
        
        self.prompt = PromptTemplate(
            input_variables=["history", "input"],
            template="""Eres un agente telefónico profesional y amable. Tu objetivo es ayudar al usuario.
            
            Historial de la conversación:
            {history}
            
            Humano: {input}
            AI: """
        )

    async def process_message(
        self,
        message: str,
        conversation_id: str | None = None,
        context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Procesa un mensaje y genera una respuesta."""
        async with self._rate_limit_semaphore:
            try:
                # 1. Recuperar historial de caché
                cached_history = await self.get_from_cache(
                    generate_conversation_cache_key(conversation_id)
                ) if conversation_id else None

                # Crear instancias temporales de memoria
                memory = ConversationBufferMemory()

                # Cargar historial de caché en la memoria temporal
                if cached_history:
                    memory.chat_memory.messages = cached_history

                # Crear instancia temporal de ConversationChain
                conversation = ConversationChain(
                    llm=self.llm,
                    memory=memory,
                    prompt=self.prompt,
                    verbose=True  # Para debug
                )

                # 2. Analizar sentimiento del mensaje
                input_sentiment = await self.analyze_sentiment(message)

                # 3. Procesar respuesta con LangChain
                response = await conversation.apredict(input=message)

                # Guardar el estado actualizado de la memoria en la caché
                await self.set_in_cache(
                    generate_conversation_cache_key(conversation_id),
                    memory.chat_memory.messages
                )

                # 4. Analizar sentimiento de la respuesta
                response_sentiment = await self.analyze_sentiment(response)

                # 5. Guardar métricas
                if conversation_id:
                    await self.save_conversation_metrics(
                        conversation_id,
                        message,
                        response,
                        input_sentiment,
                        response_sentiment
                    )

                return {
                    "response": response,
                    "input_sentiment": input_sentiment,
                    "response_sentiment": response_sentiment,
                    "conversation_id": conversation_id
                }
            except Exception as e:
                logger.error(f"Error procesando mensaje: {str(e)}")
                raise HTTPException(status_code=500, detail="Error procesando mensaje")

    async def analyze_sentiment(self, text: str) -> dict[str, Any]:
        """Analiza el sentimiento del texto."""
        output_parser = JsonOutputParser()
        prompt = PromptTemplate(
            input_variables=["text"],
            partial_variables={"format_instructions": output_parser.get_format_instructions()},
            template="""Analiza el sentimiento del siguiente texto y clasifícalo.
            Texto: {text}
            Devuelve un objeto JSON con la emoción primaria (primary_emotion) y su puntuación (score). \n{format_instructions}"""
        )

        try:
            response = await self.llm.ainvoke(prompt.format(text=text))
            return json.loads(response)
        except Exception as e:
            logger.error(f"Error al analizar el sentimiento: {e}")
            return {
                "primary_emotion": "neutral",
                "score": 0.5
            }

    async def save_conversation_metrics(
        self,
        conversation_id: str,
        message: str,
        response: str,
        input_sentiment: dict[str, Any],
        response_sentiment: dict[str, float] | None = None
    ) -> None:
        """Guarda métricas de la conversación.

        Args:
            conversation_id: ID de la conversación
            message: Mensaje del usuario
            response: Respuesta generada
            input_sentiment: Análisis de sentimiento del mensaje
            response_sentiment: Análisis de sentimiento de la respuesta
        """
        interaction_data = {
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat(),
            "message_length": len(message),
            "response_length": len(response),
            "input_sentiment": input_sentiment["primary_emotion"],
            "input_sentiment_score": input_sentiment["score"],
            "response_sentiment": response_sentiment["primary_emotion"] if response_sentiment else "neutral",
            "response_sentiment_score": response_sentiment["score"] if response_sentiment else 0.5,
        }
        await self.save_metrics_to_db(interaction_data)

    async def save_metrics_to_db(self, interaction_data: dict[str, Any]) -> None:
        """Guarda las métricas en la base de datos."""
        logger.info(f"Guardando métricas en la base de datos: {interaction_data}")
        # Implementación del guardado de métricas en la base de datos
        # Ejemplo:
        # try:
        #     data, error = await supabase_client.table("conversation_metrics").insert(interaction_data).execute()
        #     if error:
        #         logger.error(f"Error al guardar métricas en la base de datos: {error}")
        # except Exception as e:
        #     logger.error(f"Error al guardar métricas en la base de datos: {e}")
        pass

    def extract_conversation_context(
        self,
        memory: ConversationBufferMemory
    ) -> dict[str, Any]:
        """Extrae el contexto de la conversación.

        Args:
            memory: Memoria de la conversación

        Returns:
            dict[str, Any]: Contexto extraído
        """
        # Implementación de la extracción de contexto
        return {}

    async def get_from_cache(self, key: str) -> Any:
        """Recupera el valor de la caché."""
        logger.info(f"Recuperando de la caché la clave: {key}")
        # Implementación de la recuperación de la caché
        return None

    async def set_in_cache(self, key: str, value: Any) -> None:
        """Guarda el valor en la caché."""
        logger.info(f"Guardando en la caché la clave: {key} con el valor: {value}")
        # Implementación del guardado en la caché
        return None
