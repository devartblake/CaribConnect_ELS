import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# Shared properties
class UserBase(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    phone: Optional[str]
    is_active: bool = True
    is_superuser: bool = False
    locale: Optional[str] = "en_US"
    full_name: Optional[str] = Field(None, max_length=255)

# Properties to receive via API on creation
class UserCreateSchema(UserBase):
    password: str = Field(..., min_length=8, max_length=40)

# User registration schema, for public access with optional phone
class UserRegisterSchema(UserBase):
    password: str = Field(..., min_length=8, max_length=40)
    phone: Optional[str] = Field(None, max_length=15)

# User update schema
class UserUpdateSchema(UserBase):
    email: Optional[EmailStr] = Field(None, max_length=255)
    password: Optional[str] = Field(None, min_length=8, max_length=40)

class UserUpdateMeSchema(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class UpdatePasswordSchema(BaseModel):
    current_password: str
    new_password: str

class UserReadSchema(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

# Properties to return via API, public-facing
class UserPublic(UserBase):
    id: uuid.UUID

class UsersPublic(UserBase):
    data: list[UserPublic]
    count: int

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[str] = None

class NewPassword(BaseModel):
    token: str
    new_password: str

class Config:
    from_attributes = True
