from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class ClientBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    phone: str = Field(..., min_length=10, max_length=50)
    email: EmailStr | None = None
    notes: str | None = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    phone: str | None = Field(None, min_length=10, max_length=50)
    email: EmailStr | None = None
    notes: str | None = None


class Client(ClientBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
