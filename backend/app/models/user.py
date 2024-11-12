import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union

from pydantic import EmailStr
from sqlalchemy import JSON
from .otp import OTP
from .items import Item
from .payments import Payment
from .professional import Professional
from .engagment_metrics import PageView, SocialConnection, Post, Comment
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=15)  # Add phone field

# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)

class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)

class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)

# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    user_roles: list["UserRole"] = Relationship(back_populates="user", cascade_delete=True)
    addresses: list["UserAddress"] = Relationship(back_populates="user", cascade_delete=True)
    payments: list["Payment"] = Relationship(back_populates="user", cascade_delete=True)
    page_views: list["PageView"] = Relationship(back_populates="user", cascade_delete=True)
    social_connections: list["SocialConnection"] = Relationship(back_populates="user", cascade_delete=True)
    posts: list["Post"] = Relationship(back_populates="author", cascade_delete=True)
    comments: list["Comment"] = Relationship(back_populates="user", cascade_delete=True)
    professionals: list["Professional"] = Relationship(back_populates="user") # Relationship to Professional
    otps: list["OTP"] = Relationship(back_populates="user")

# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

# New UserAddress Model
class UserAddress(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    address_line_1: str = Field(max_length=255)
    address_line_2: str | None = Field(default=None, max_length=255)
    city: str = Field(max_length=255)
    state: str = Field(max_length=255)
    country: str = Field(max_length=255)
    postal_code: str = Field(max_length=20)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)
    phone: Optional[str] = Field(default=None, max_length=15)  # Add phone field
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    # Relationship back to User
    user: User = Relationship(back_populates="addresses")

# User Role-based Access Control (RBAC)
class UserRole(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    role: str = Field(max_length=50) # 'staff', 'client', 'professional'
    sub_role: str | None = Field(max_length=50, default=None) # Optional for further sub-credentials
    user: User = Relationship(back_populates="user_roles")
    
# Generic message
class Message(SQLModel):
    message: str

# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None

class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)

# Define an Enum for record types or report categories if needed
class RecordType(str, Enum):
    TYPE_A = "Type A"
    TYPE_B = "Type B"

# Define the Record model
class Record(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    record_type: RecordType
    created_at: datetime = Field(default_factory=datetime.utcnow)
    data: str | None = Field(default=None, max_length=255)
