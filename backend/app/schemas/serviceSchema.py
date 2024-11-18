from pydantic import BaseModel
from typing import Optional
import uuid

class ServiceBase(BaseModel):
    name: str
    description: Optional[str]

class ServiceCreate(ServiceBase):
    professional_id: Optional[uuid.UUID]

class ServiceUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    professional_id: Optional[uuid.UUID]

class ServiceRead(ServiceBase):
    id: uuid.UUID
    professional_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True