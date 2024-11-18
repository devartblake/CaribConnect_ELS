from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import uuid

# Address schema for validation and API responses
class UserAddressBase(BaseModel):
    address_line_1: str = Field(..., max_length=255)
    address_line_2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., max_length=255)
    state: str = Field(..., max_length=255)
    country: str = Field(..., max_length=255)
    postal_code: str = Field(..., max_length=20)
    latitude: Optional[float]
    longitude: Optional[float]
    phone: Optional[str] = Field(None, max_length=15)

class UserAddressCreate(UserAddressBase):
    pass

class UserAddressUpdate(UserAddressBase):
    address_line_1: Optional[str] = Field(None, max_length=255)

class UserAddressPublic(UserAddressBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
