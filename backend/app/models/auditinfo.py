import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class AuditInfo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    action: str
    description: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default=None)
    user_id: uuid.UUID | None = Field(foreign_key="user.id")

    # Back-populate relationship to User
    user: Optional["User"] = Relationship(back_populates="audit_info")

class AuditInfoCreate(SQLModel):
    user_id: uuid.UUID
    action_type: str
    action_description: str | None = None

class AuditInfoUpdate(SQLModel):
    action_type: str | None = None
    action_description: str | None = None
