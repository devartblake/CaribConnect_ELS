from decimal import Decimal
from typing import Optional
import uuid
from pydantic import BaseModel

class ExchangeRateBase(BaseModel):
    rate: Decimal
    timestamp: Optional[str]  # ISO 8601 timestamp for when the rate was fetched
    base_currency_id: uuid.UUID
    target_currency_id: uuid.UUID

class ExchangeRateCreateSchema(ExchangeRateBase):
    pass

class ExchangeRateUpdateSchema(ExchangeRateBase):
    rate: Optional[Decimal] = None
    timestamp: Optional[str] = None

class ExchangeRateReadSchema(ExchangeRateBase):
    id: uuid.UUID

    class Config:
        from_attributes = True