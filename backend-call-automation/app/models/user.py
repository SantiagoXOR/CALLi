from enum import Enum

from pydantic import BaseModel, EmailStr

from .base import BaseDBModel


class UserRole(str, Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    role: UserRole | None = None
    password: str | None = None
    is_active: bool | None = None


class User(BaseDBModel, UserBase):
    pass
