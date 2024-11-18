import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, Union

from pydantic import EmailStr
from sqlalchemy import JSON
from sqlmodel import Column, Field, Relationship, SQLModel
from .customizationinfo import CustomizationInfo  # Import CustomizationInfo if it's in a separate module

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
    first_name: str | None = Field(default=None, max_length=20)
    last_name: str | None = Field(default=None, max_length=20)
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

class Territory(SQLModel, table=True) :
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    manager: bool    
    user_id: int = Field(foreign_key="user.id")
    # Relationships
    users: Optional["User"] = Relationship(back_populates="territories")
    
# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

# Database model, database table inferred from class name
class User(UserBase, table=True):    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    full_name: Optional[str] = Field(default=None, max_length=255)
    otp_codes: list["OTP"] = Relationship(back_populates="user")
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    addresses: list["UserAddress"] = Relationship(back_populates="user", cascade_delete=True)
    payments: list["Payment"] = Relationship(back_populates="user")
    page_views: list["PageView"] = Relationship(back_populates="user")
    social_connections: list["SocialConnection"] = Relationship(back_populates="user", cascade_delete=True)
    posts: list["Post"] = Relationship(back_populates="author", cascade_delete=True)
    comments: list["Comment"] = Relationship(back_populates="user", cascade_delete=True)
    professionals: list["Professional"] = Relationship(back_populates="user") # Relationship to Professional
    audit_info: Optional["AuditInfo"] = Relationship(back_populates="user")
    customize_info: Optional["CustomizationInfo"] = Relationship(back_populates="user", sa_relationship_kwargs={"foreign_keys": [CustomizationInfo.user_id]})
    # Relationship to UserRole
    user_roles: list["UserRole"] = Relationship(back_populates="user")
    # Relationship with Territory
    territories: list["Territory"] = Relationship(back_populates="users")
    
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
    language: Optional[list[str]] = Field(default=[], sa_column=Column(JSON))
    locale: str
    audit_info_id: Optional[int] = Field(default=None, foreign_key="auditinfo.id") # Relationship with AuditInfo
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    # Relationship back to User
    user: User = Relationship(back_populates="addresses")

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
