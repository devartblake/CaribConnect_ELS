import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union

from pydantic import EmailStr
from sqlalchemy import JSON
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

class Professional(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    profession: str = Field(max_length=255, index=True, nullable=False)
    description: str | None = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)
    experience_years: int | None = Field(default=None)
    # Foreign key to the User model
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # Use SQLAlchemy's Column with onupdate
    updated_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))

    # Relationship back to User
    user: "User" = Relationship(back_populates="professionals")
    # Relationships back to Services
    services: list["Service"] = Relationship(back_populates="professionals")

class ProfessionalCreate(SQLModel):
    name: str
    specialization: str
    experience_years: Optional[int] = None
    user_id: uuid.UUID

class ProfessionalUpdate(SQLModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
