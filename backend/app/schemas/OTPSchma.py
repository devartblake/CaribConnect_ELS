from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class OTPCreateSchema(BaseModel):
    otp_code: str
    expires_at: datetime

class OTPResponseSchema(BaseModel):
    id: int
    otp_code: str
    created_at: datetime
    expires_at: datetime
    attempts: int
    user_id: int

    class Config:
        from_attributes = True  # Enables SQLModel compatibility with Pydantic v2