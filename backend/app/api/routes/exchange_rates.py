import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.db import get_database_session
from app.models import ExchangeRate
from app.schemas.exchangeRateSchema import (
    ExchangeRateCreateSchema,
    ExchangeRateUpdateSchema,
)
from app.services.exchange_rate_service import ExchangeRateService
from app.workers.celery_worker import celery_worker as celery_app

router = APIRouter()

# Dependency to provide the service
@router.get("/exchange-rates")
def get_exchange_rate_service(db_session: Session = Depends(get_database_session)):
    return db_session.exec(ExchangeRate).all()

# Get all exchange rates
@router.get("/", response_model=list[ExchangeRate])
async def get_all_exchange_rates(service: ExchangeRateService = Depends(get_exchange_rate_service)):
    return service.get_all_exchange_rates()

# Get exchange rate by ID
@router.get("/{exchange_rate_id}", response_model=ExchangeRate)
async def get_exchange_rate_by_id(
    exchange_rate_id: uuid.UUID,
    service: ExchangeRateService = Depends(get_exchange_rate_service),
):
    """
    Retrieve an exchange rate by its ID.
    """
    exchange_rate = service.get_exchange_rate_by_id(exchange_rate_id)
    if not exchange_rate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exchange rate not found",
        )
    return exchange_rate

# Create a new exchange rate
@router.post("/", response_model=ExchangeRate, status_code=status.HTTP_201_CREATED)
async def create_exchange_rate(
    exchange_rate_data: ExchangeRateCreateSchema,
    service: ExchangeRateService = Depends(get_exchange_rate_service),
):
    """
    Create a new exchange rate.
    """
    return service.create_exchange_rate(exchange_rate_data)

# Update exchange rate by ID
@router.put("/{exchange_rate_id}", response_model=ExchangeRate)
async def update_exchange_rate(
    exchange_rate_id: uuid.UUID,
    exchange_rate_data: ExchangeRateUpdateSchema,
    service: ExchangeRateService = Depends(get_exchange_rate_service),
):
    """
    Update an existing exchange rate.
    """
    updated_exchange_rate = service.update_exchange_rate(exchange_rate_id, exchange_rate_data)
    if not updated_exchange_rate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exchange rate not found",
        )
    return updated_exchange_rate

# Delete exchange rate by ID
@router.delete("/{exchange_rate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exchange_rate(
    exchange_rate_id: uuid.UUID,
    service: ExchangeRateService = Depends(get_exchange_rate_service),
):
    """
    Delete an exchange rate by its ID.
    """
    success = service.delete_exchange_rate(exchange_rate_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exchange rate not found"
        )
    return {"detail": "Exchange rate deleted"}

@router.post("/update", status_code=status.HTTP_202_ACCEPTED)
def update_exchange_rates(service: ExchangeRateService = Depends(get_exchange_rate_service)):
    """
    Update all exchange rates from the external API.
    """
    service.update_exchange_rates()
    return {"message": "Exchange rates updated successfully"}


@router.post("/schedule-update", status_code=status.HTTP_202_ACCEPTED)
def schedule_exchange_rate_update(service: ExchangeRateService = Depends(get_exchange_rate_service)):
    """
    Schedule an asynchronous task to update exchange rates using Celery.
    """
    service.schedule_update_exchange_rates()
    return {"message": "Exchange rate update task scheduled"}
