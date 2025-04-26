from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.call_service import CallService

router = APIRouter()

@router.websocket("/ws/call/{call_id}")
async def websocket_endpoint(websocket: WebSocket, call_id: str):
    """
    Endpoint WebSocket para manejar llamadas en tiempo real.
    
    Args:
        websocket: La conexión WebSocket.
        call_id: El ID de la llamada.
    """
    await websocket.accept()
    call_service = CallService()
    
    try:
        # Iniciar llamada
        await call_service.start_call(call_id)
        
        while True:
            # Recibir audio/texto del cliente
            user_message = await websocket.receive_text()
            
            # Procesar y generar respuesta
            audio_response = await call_service.handle_call_response(
                call_id=call_id,
                user_message=user_message
            )
            
            # Enviar respuesta de audio
            await websocket.send_bytes(audio_response)
            
    except WebSocketDisconnect:
        # Finalizar llamada cuando se desconecta
        await call_service.end_call(call_id)

@router.websocket("/ws/call/{call_id}/audio")
async def audio_websocket_endpoint(websocket: WebSocket, call_id: str):
    """
    Endpoint WebSocket para manejar streaming de audio bidireccional.
    
    Args:
        websocket: La conexión WebSocket.
        call_id: El ID de la llamada.
    """
    await websocket.accept()
    call_service = CallService()
    
    try:
        # Iniciar llamada
        await call_service.start_call(call_id)
        
        # Configurar parámetros de streaming
        await call_service.elevenlabs_service.configure_stream_settings({
            'chunk_size': 1024,
            'latency': 'low',
            'quality': 'high'
        })
        
        while True:
            # Recibir chunks de audio
            audio_chunk = await websocket.receive_bytes()
            
            # Procesar audio y generar respuesta
            response_chunk = await call_service.handle_audio_stream(
                call_id=call_id,
                audio_chunk=audio_chunk
            )
            
            # Enviar chunk de respuesta
            await websocket.send_bytes(response_chunk)
            
    except WebSocketDisconnect:
        # Finalizar llamada cuando se desconecta
        await call_service.end_call(call_id)
    except Exception as e:
        # Manejar otros errores
        import logging
        logging.error(f"Error en websocket de audio: {str(e)}")
        await call_service.end_call(call_id)
        raise
