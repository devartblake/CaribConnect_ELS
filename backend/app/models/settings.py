import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, Union

from pydantic import EmailStr
from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel

# Settings
class Settings(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    notifications_enabled: bool = True
    theme: Optional[str] = Field(default="light")
    language: Optional[str] = Field(default="en")    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)

    # Relationship back to User
    user: Optional["User"] = Relationship(back_populates="settings")
    
class SettingsCreate(SQLModel):
    notifications_enabled: bool = True
    theme: Optional[str] = "light"
    language: Optional[str] = "en"
    user_id: uuid.UUID

class SettingsUpdate(SQLModel):
    notifications_enabled: Optional[bool] = None
    theme: Optional[str] = None
    language: Optional[str] = None

class SettingsDelete(SQLModel):
    id: uuid.UUID
    
# Status
class Status(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    is_online: bool = Field(default=False)
    last_active: Optional[str] = Field(default=None)
    user_id: uuid.UUID = Field(foreign_key="user.id")

    # Relationship back to User
    user: Optional["User"] = Relationship(sa_relationship_kwargs={"lazy": "joined"})
    
class StatusCreate(SQLModel):
    is_online: bool = False
    last_active: Optional[str] = None
    user_id: uuid.UUID

class StatusUpdate(SQLModel):
    is_online: Optional[bool] = None
    last_active: Optional[str] = None

class StatusDelete(SQLModel):
    id: uuid.UUID
    