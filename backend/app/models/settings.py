import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel


# Settings
class Settings(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    notifications_enabled: bool = True
    theme: Optional[str] = Field(default="light")
    language: Optional[str] = Field(default="en")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    status_id: uuid.UUID = Field(foreign_key="status.id")

    # Relationship back to User
    user: Optional["User"] = Relationship(back_populates="settings")
    status: Optional["Status"] = Relationship(back_populates="settings")

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
