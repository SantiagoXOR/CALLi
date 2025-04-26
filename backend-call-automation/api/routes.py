from fastapi import APIRouter, HTTPException
from services.twilio_service import TwilioService
from services.supabase_service import SupabaseService
from typing import Dict

router = APIRouter()
twilio_service = TwilioService()
supabase_service = SupabaseService()

@router.post("/calls/")
async def make_call(data: Dict[str, str]):
    try:
        phone_number = data.get("phone_number")
        if not phone_number:
            raise HTTPException(status_code=400, detail="Phone number is required")
            
        # Iniciar llamada con Twilio
        call = twilio_service.make_call(phone_number)
        
        # Guardar registro en Supabase
        call_record = await supabase_service.save_call_record({
            "phone_number": phone_number,
            "status": call.status,
            "sid": call.sid
        })
        
        return {
            "status": "success",
            "call_sid": call.sid,
            "record_id": call_record.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
