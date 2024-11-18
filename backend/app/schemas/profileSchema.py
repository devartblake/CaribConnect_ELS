from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

# Shared properties
class ProfileBase(BaseModel):
    display_label: str
    name: str
    description: Optional[str]
    category: Optional[bool] = False

# Properties to receive via API on creation
class ProfileCreateSchema(ProfileBase):
    created_by_user_id: Optional[uuid.UUID]

class ProfileReadSchema(ProfileBase):
    id: uuid.UUID
    created_time: Optional[datetime]
    modified_time: Optional[datetime]

# Properties to receive via API on update
class ProfileUpdateSchema(ProfileBase):
    modified_time: datetime
    modified_by_user_id: uuid.UUID

# Properties to return via API
class ProfilePublic(ProfileBase):
    id: uuid.UUID