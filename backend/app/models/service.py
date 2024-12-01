import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import JSON, Numeric
from sqlmodel import Column, Field, Relationship, SQLModel

from .professional import Professional


# Professional & Service Models
class Service(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    category: str = Field(max_length=100)
    tags: list[str] = Field(sa_column=Column(JSON))
    price: Decimal = Field(..., sa_column=Column(Numeric(10, 2)))
    currency_id: uuid.UUID = Field(..., foreign_key="currency.id")
    user_id: uuid.UUID = Field(..., foreign_key="user.id")
    location: Optional[str] = Field(max_length=255)
    status: str = Field(default="available", max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    image_url: Optional[str] = None
    average_rating: Optional[float] = Field(default=0.0, ge=0.0, le=5.0)
    reviews_count: int = Field(default=0)

    # Relationships
    currency: "Currency" = Relationship(back_populates="services")
    professional_id: int | None = Field(foreign_key="professional.id")
    professionals: "Professional" = Relationship(back_populates="services")
