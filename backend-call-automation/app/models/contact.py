from typing import Optional, List, Annotated
from pydantic import BaseModel, EmailStr, Field
from .base import BaseDBModel

class ContactBase(BaseModel):
    name: str
    phone_number: Annotated[str, Field(pattern=r'^\+?1?\d{9,15}$')]  # International phone number format
    email: Optional[EmailStr] = None
    notes: Optional[str] = None
    tags: List[str] = []

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    name: Optional[str] = None
    phone_number: Optional[str] = None

class Contact(BaseDBModel, ContactBase):
    pass

class ContactListBase(BaseModel):
    name: str
    description: Optional[str] = None

class ContactListCreate(ContactListBase):
    contacts: List[str] = []  # List of contact IDs

class ContactList(BaseDBModel, ContactListBase):
    contacts: List[Contact] = []
