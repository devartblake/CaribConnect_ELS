import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class AuditInfo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    action: str
    description: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    user_id: Optional[uuid.UUID] = Field(foreign_key="user.id")
    
    # Back-populate relationship to User
    user: Optional["User"] = Relationship(back_populates="audit_info")

class AuditInfoCreate(SQLModel):
    user_id: uuid.UUID
    action_type: str
    action_description: Optional[str] = None
    
class AuditInfoUpdate(SQLModel):
    action_type: Optional[str] = None
    action_description: Optional[str] = None
    