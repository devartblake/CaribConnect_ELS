from decimal import Decimal
import uuid
from pydantic import BaseModel, Field
from typing import Optional

class CurrencyBase(BaseModel):
    name: str
    iso_code: str
    symbol: str
    exchange_rate: Decimal
    prefix_symbol: bool = Field(default=True)
    is_active: bool = Field(default=True)

class CurrencyCreate(CurrencyBase):
    pass

class CurrencyUpdate(BaseModel):
    name: Optional[str]
    iso_code: Optional[str]
    symbol: Optional[str]
    exchange_rate: Optional[Decimal]
    prefix_symbol: Optional[bool]
    is_active: Optional[bool]

class CurrencyRead(CurrencyBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
        
class CurrencyFormatSchema(BaseModel):
    decimal_separator: str = Field(..., max_length=10, example="Period")
    thousand_separator: str = Field(..., max_length=10, example="Comma")
    decimal_places: int = Field(..., ge=0, le=10, example=2)

class CurrencySchema(BaseModel):
    name: str = Field(..., max_length=100, example="Saudi Riyal - SAR")
    iso_code: str = Field(..., max_length=3, example="SAR")
    symbol: str = Field(..., max_length=10, example="SR")
    exchange_rate: Decimal = Field(..., max_digits=10, decimal_places=7, example=1.0000000)
    prefix_symbol: bool = Field(default=True, example=True)
    is_active: bool = Field(default=True, example=True)
    format: Optional[CurrencyFormatSchema]

    class Config:
        orm_mode = True
