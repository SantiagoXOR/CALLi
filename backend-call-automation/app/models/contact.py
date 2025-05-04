from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from .base import BaseDBModel


class ContactBase(BaseModel):
    name: str
    phone_number: Annotated[
        str, Field(pattern=r"^\+?1?\d{9,15}$")
    ]  # International phone number format
    email: EmailStr | None = None
    notes: str | None = None
    tags: list[str] = Field(default_factory=list)


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    name: str | None = None
    phone_number: Annotated[str, Field(pattern=r"^\+?1?\d{9,15}$")] | None = None
    email: EmailStr | None = None
    notes: str | None = None
    tags: list[str] | None = None


class Contact(BaseDBModel, ContactBase):
    pass


class ContactListBase(BaseModel):
    name: str
    description: str | None = None


class ContactListCreate(ContactListBase):
    contacts: list[str] = Field(default_factory=list)  # List of contact IDs


class ContactList(BaseDBModel, ContactListBase):
    contacts: list[Contact] = Field(default_factory=list)
