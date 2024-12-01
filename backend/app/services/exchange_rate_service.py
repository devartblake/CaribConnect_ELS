import uuid
from datetime import datetime
from typing import Optional

import requests
from celery import Celery
from fastapi import logger
from sqlmodel import Session

from app.core.config import settings
from app.core.db import SessionLocal, get_database_session
from app.models import ExchangeRate  # Adjust based on your project
from app.schemas.exchangeRateSchema import (
    ExchangeRateCreateSchema,
    ExchangeRateUpdateSchema,
)
from app.workers.celery_worker import celery_worker


class ExchangeRateService:
    """
    Service for managing exchange rates. Handles fetching, updating, and maintaining exchange rate data.
    """

    def __init__(self, db_session: Session = None, celery_app: Celery = None):
        """
        Initialize the service with dependencies.

        Args:
            db_session (Session): Database session for interacting with the database.
            celery_app (Celery): Celery app for background task management.
        """
        self.db_session = db_session
        self.celery_app = celery_app

    def test_exchange_rate_service():
        # Use the generator to get the session
        db_session = SessionLocal()
        try:
            exchange_rate_service = ExchangeRateService(db_session=db_session, celery_app=celery_worker)

            # Perform operations
            exchange_rate_service.update_exchange_rates()
            exchange_rate_service.schedule_update_exchange_rates()
        finally:
            db_session.close()

    # -----------------
    # Public Methods
    # -----------------

    def get_exchange_rate(self, url: str) -> dict[str, float]:
        """
        Fetch exchange rates from an external API.

        Args:
            url (str): URL of the exchange rate API.

        Returns:
            dict[str, float]: Dictionary of currency codes and their rates.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("rates", {})
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch exchange rates: {e}")

    def update_exchange_rates(self):
        """
        Fetch and update exchange rates in the database.
        """
        rates = self.get_exchange_rate(settings.EXCHANGE_RATE_URI)
        for currency, rate in rates.items():
            existing_rate = (
                self.db_session.query(ExchangeRate)
                .filter_by(currency=currency)
                .first()
            )
            if existing_rate:
                existing_rate.rate = rate
                existing_rate.last_updated = datetime.utcnow()
            else:
                new_rate = ExchangeRate(currency=currency, rate=rate)
                self.db_session.add(new_rate)
        self.db_session.commit()  # Commit after the changes

    def schedule_update_exchange_rates(self):
        """
        Schedule the `update_exchange_rates` task to run in the background using Celery.
        """
        self.celery_app.send_task("tasks.update_exchange_rates_task")

    def get_all_exchange_rates(self) -> list[ExchangeRate]:
        """
        Retrieve all exchange rates from the database.

        Returns:
            List[ExchangeRate]: A list of exchange rate objects.
        """
        return self.db_session.query(ExchangeRate).all()

    def get_exchange_rate_by_id(self, exchange_rate_id: uuid.UUID) -> Optional[ExchangeRate]:
        """
        Retrieve an exchange rate by its ID.

        Args:
            exchange_rate_id (uuid.UUID): The ID of the exchange rate.

        Returns:
            Optional[ExchangeRate]: The exchange rate object, if found.
        """
        return self.db_session.get(ExchangeRate, exchange_rate_id)

    def create_exchange_rate(self, exchange_rate_data: ExchangeRateCreateSchema) -> ExchangeRate:
        """
        Create a new exchange rate entry in the database.

        Args:
            exchange_rate_data (ExchangeRateCreateSchema): Data for creating a new exchange rate.

        Returns:
            ExchangeRate: The newly created exchange rate object.
        """
        new_exchange_rate = ExchangeRate.from_orm(exchange_rate_data)
        self.db_session.add(new_exchange_rate)
        self.db_session.commit()
        self.db_session.refresh(new_exchange_rate)
        return new_exchange_rate

    def update_exchange_rate(
        self, exchange_rate_id: uuid.UUID, exchange_rate_data: ExchangeRateUpdateSchema
    ) -> Optional[ExchangeRate]:
        """
        Update an existing exchange rate.

        Args:
            exchange_rate_id (uuid.UUID): The ID of the exchange rate to update.
            exchange_rate_data (ExchangeRateUpdateSchema): The updated data.

        Returns:
            Optional[ExchangeRate]: The updated exchange rate object, if found.
        """
        existing_rate = self.get_exchange_rate_by_id(exchange_rate_id)
        if not existing_rate:
            return None
        update_data = exchange_rate_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing_rate, field, value)
        self.db_session.commit()
        self.db_session.refresh(existing_rate)
        return existing_rate

    def delete_exchange_rate(self, exchange_rate_id: uuid.UUID) -> bool:
        """
        Delete an exchange rate by its ID.

        Args:
            exchange_rate_id (uuid.UUID): The ID of the exchange rate to delete.

        Returns:
            bool: True if the exchange rate was deleted, False otherwise.
        """
        existing_rate = self.get_exchange_rate_by_id(exchange_rate_id)
        if not existing_rate:
            return False
        self.db_session.delete(existing_rate)
        self.db_session.commit()
        return True
