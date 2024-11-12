import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union

from pydantic import EmailStr
from sqlalchemy import JSON
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

class OTP(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    otp_code: str = Field(max_length=6)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    attempts: int = Field(default=0)
    user_id: int = Field(foreign_key="user.id")

    user: Optional["User"] = Relationship(back_populates="otps")