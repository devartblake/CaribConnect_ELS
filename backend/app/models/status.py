import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


# Status
class Status(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    online: bool = Field(default=False)
    last_ip: Optional[str] = Field(default=None, max_length=45)
    device: Optional[str] = Field(default=None, max_length=100)
    last_seen: datetime = Field(default_factory=datetime.utcnow)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="status")
    settings: Optional["Settings"] = Relationship(back_populates="status") 

class StatusCreate(SQLModel):
    is_online: bool = False
    last_active: Optional[str] = None
    user_id: uuid.UUID

class StatusUpdate(SQLModel):
    is_online: Optional[bool] = None
    last_active: Optional[str] = None

class StatusDelete(SQLModel):
    id: uuid.UUID
