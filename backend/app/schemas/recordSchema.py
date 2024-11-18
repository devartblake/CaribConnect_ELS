from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
import uuid

# Enum for record types
class RecordType(str, Enum):
    TYPE_A = "Type A"
    TYPE_B = "Type B"

# Record schema for data validation
class RecordBase(BaseModel):
    record_type: RecordType
    data: Optional[str] = Field(None, max_length=255)

class RecordCreate(RecordBase):
    pass

class RecordUpdate(RecordBase):
    record_type: Optional[RecordType]

class RecordPublic(RecordBase):
    id: uuid.UUID
    created_at: datetime
