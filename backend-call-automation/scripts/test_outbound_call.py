import asyncio
import sys
from app.services.elevenlabs_service import ElevenLabsService
from app.config.settings import settings

async def test_outbound_call(phone_number: str):
    """
    Script para probar una llamada saliente.
    
    Uso:
        python test_outbound_call.py +1234567890
    """
    service = ElevenLabsService()
    
    try:
        response = await service.initiate_outbound_call(
            to_number=phone_number,
            prompt="Hola, esta es una llamada de prueba.",
            metadata={"test_call": True}
        )
        print(f"Llamada iniciada exitosamente: {response}")
        
    except Exception as e:
        print(f"Error al iniciar la llamada: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python test_outbound_call.py +1234567890")
        sys.exit(1)
        
    asyncio.run(test_outbound_call(sys.argv[1]))
