from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict


class BaseDBModel(BaseModel):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
