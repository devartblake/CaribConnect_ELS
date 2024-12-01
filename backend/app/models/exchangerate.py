import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Numeric
from sqlmodel import Column, Field, Relationship, SQLModel


class ExchangeRate(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    base_currency_id: uuid.UUID = Field(foreign_key="currency.id")
    target_currency_id: uuid.UUID = Field(foreign_key="currency.id")
    rate: Decimal = Field(..., sa_column=Column(Numeric(10, 7)))
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    base_currency: "Currency" = Relationship(sa_relationship_kwargs={"foreign_keys": "ExchangeRate.base_currency_id"})
    target_currency: "Currency" = Relationship(sa_relationship_kwargs={"foreign_keys": "ExchangeRate.target_currency_id"})
