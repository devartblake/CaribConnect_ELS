import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, Relationship


# Settings
class Settings(BaseModel):
    notifications_enabled: bool = Field(default=True)
    theme: Optional[str] = Field(default="light")
    language: Optional[str] = Field(default="en")
    user_id: uuid.UUID

    # Relationship back to User
    user: Optional["User"] = Relationship(back_populates="settings")

class SettingsCreateSchema(BaseModel):
    notifications_enabled: Optional[bool] = Field(default=True)
    theme: Optional[str] = Field(default="light")
    language: Optional[str] = Field(default="en")

class SettingsUpdateSchema(BaseModel):
    notifications_enabled: Optional[bool] = None
    theme: Optional[str] = None
    language: Optional[str] = None

class SettingsDeleteSchema(BaseModel):
    id: uuid.UUID

# Status Schema
class StatusBase(BaseModel):
    online: bool
    last_ip: Optional[str]
    device: Optional[str]

class StatusCreateSchema(StatusBase):
    pass

class StatusUpdateSchema(StatusBase):
    online: Optional[bool] = None

class StatusReadSchema(StatusBase):
    id: uuid.UUID
    last_seen: datetime

class Config:
    from_attributes = True
