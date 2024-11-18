from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session
from app.models import Currency
from app.schemas.currencySchema import (
    CurrencyCreate,
    CurrencyRead,
    CurrencyUpdate,
)
from app.api.deps import get_db
from typing import List
import uuid

router = APIRouter()

# Get all currencies
@router.get("/", response_model=List[CurrencyRead])
async def get_all_currencies(session: Session = Depends(get_db)):
    currencies = session.query(Currency).all()
    return currencies

# Get currency by ID
@router.get("/{currency_id}", response_model=CurrencyRead)
async def get_currency(currency_id: uuid.UUID, session: Session = Depends(get_db)):
    currency = session.get(Currency, currency_id)
    if not currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")
    return currency

# Create a new currency
@router.post("/", response_model=CurrencyRead, status_code=status.HTTP_201_CREATED)
async def create_currency(currency_data: CurrencyCreate, session: Session = Depends(get_db)):
    currency = Currency.form_orm(currency_data)
    session.add(currency)
    session.commit()
    session.refresh(currency)
    return currency

# Update currency by ID
@router.put("/{currency_id}", response_model=CurrencyRead)
async def update_currency(currency_id: uuid.UUID, currency_data: CurrencyUpdate, session: Session = Depends(get_db)):
    existing_currency = session.get(Currency, currency_id)
    if not existing_currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")
    update_data = currency_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing_currency, field, value)
    session.add(existing_currency)
    session.commit()
    session.refresh(existing_currency)
    return existing_currency

# Delete currency by ID
@router.delete("/{currency_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_currency(currency_id: uuid.UUID, session: Session = Depends(get_db)):
    currency = session.get(Currency, currency_id)
    if not currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")
    session.delete(currency)
    session.commit()
    return {"detail": "Currency deleted"}
