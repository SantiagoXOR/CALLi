from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4, ConfigDict

class BaseDBModel(BaseModel):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
