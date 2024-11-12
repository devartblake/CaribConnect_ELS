import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union

from pydantic import EmailStr
from sqlalchemy import JSON
from .professional import Professional
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

# Professional & Service Models
class Service(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    professional_id: int | None = Field(foreign_key="professional.id")
    professionals: "Professional" = Relationship(back_populates="services")
