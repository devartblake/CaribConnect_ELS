from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

class AuditInfoBase(BaseModel):
    user_id: UUID
    action: str
    timestamp: Optional[str] = Field(None, description="ISO 8601 format")

class AuditInfoCreate(AuditInfoBase):
    pass

class AuditInfoRead(AuditInfoBase):
    id: UUID
