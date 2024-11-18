import uuid
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional

# Settings
class Settings(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    notifications_enabled: bool = Field(default=True)
    theme: Optional[str] = Field(default="light")
    language: Optional[str] = Field(default="en")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)

    # Relationship back to User
    user: Optional["User"] = Relationship(back_populates="settings")

class SettingsCreateSchema(SQLModel):
    notifications_enabled: Optional[bool] = Field(default=True)
    theme: Optional[str] = Field(default="light")
    language: Optional[str] = Field(default="en")
    user_id: uuid.UUID

class SettingsUpdateSchema(SQLModel):
    notifications_enabled: Optional[bool] = None
    theme: Optional[str] = None
    language: Optional[str] = None

class SettingsDeleteSchema(SQLModel):
    id: uuid.UUID

# Status Schema
class Status(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    is_online: bool = Field(default=False)
    last_active: Optional[datetime] = None
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)

class StatusCreateSchema(SQLModel):
    is_online: bool = Field(default=False)
    last_active: Optional[datetime] = None
    user_id: uuid.UUID

class StatusUpdateSchema(SQLModel):
    is_online: Optional[bool] = None
    last_active: Optional[datetime] = None

class StatusDeleteSchema(SQLModel):
    id: uuid.UUID