from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
import uuid

# Shared properties
class UserBase(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = Field(None, max_length=255)

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=40)

# User registration schema, for public access with optional phone
class UserRegister(UserBase):
    password: str = Field(..., min_length=8, max_length=40)
    phone: Optional[str] = Field(None, max_length=15)
    
# User update schema
class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(None, max_length=255)
    password: Optional[str] = Field(None, min_length=8, max_length=40)

class UserUpdateMe(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class UpdatePassword(BaseModel):
    current_password: str
    new_password: str

# Properties to return via API, public-facing
class UserPublic(UserBase):
    id: uuid.UUID

class UsersPublic(BaseModel):
    data: List[UserPublic]
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