from decimal import Decimal
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union

from pydantic import EmailStr
from sqlalchemy import JSON, Numeric
from .professional import Professional
from sqlmodel import Column, Field, Relationship, SQLModel

# Professional & Service Models
class Service(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    category: str = Field(max_length=100)
    tags: list[str] = Field(sa_column=Column(JSON))
    price: Decimal = Field(..., sa_column=Column(Numeric(10, 2)))
    location: Optional[str] = Field(max_length=255)
    status: str = Field(default="available", max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    image_url: Optional[str] = None
    average_rating: Optional[float] = Field(default=0.0, ge=0.0, le=5.0)
    reviews_count: int = Field(default=0)
    
    professional_id: int | None = Field(foreign_key="professional.id")
    professionals: "Professional" = Relationship(back_populates="services")
