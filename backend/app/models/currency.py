import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import JSON, Numeric
from sqlmodel import Column, Field, Relationship, SQLModel


class Currency(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(..., max_length=100, index=True)
    iso_code: str = Field(..., max_length=3, unique=True)
    symbol: str = Field(..., max_length=10)
    exchange_rate: Decimal = Field(..., sa_column=Column(Numeric(10, 7)))
    prefix_symbol: bool = Field(default=True)
    is_active: bool = Field(default=True)

    # Reverse Relationships
    services: list["Service"] = Relationship(back_populates="currency")

    # Relationship to format settings
    format_id: uuid.UUID | None = Field(default=None, foreign_key="currencyformat.id")
    format: "CurrencyFormat" = Relationship(back_populates="currency")

    # Reverse relationships
    base_exchange_rates: list["ExchangeRate"] = Relationship(back_populates="base_currency", sa_relationship_kwargs={"foreign_keys": "ExchangeRate.base_currency_id"},)
    target_exchange_rates: list["ExchangeRate"] = Relationship(back_populates="target_currency", sa_relationship_kwargs={"foreign_keys": "ExchangeRate.target_currency_id"},)

class CurrencyFormat(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    decimal_separator: str = Field(..., max_length=10)
    thousand_separator: str = Field(..., max_length=10)
    decimal_places: int = Field(..., ge=0, le=10)

    # Reverse relationship
    currency: "Currency" = Relationship(back_populates="format")
