from celery import Celery
from sqlalchemy.orm import Session

from app.models import ExchangeRate

# Define the Celery app for background tasks
celery_app = Celery("tasks", broker="redis://redis:6379/0")

# Celery task
@celery_app.task(name="tasks.update_exchange_rate")
def update_exchange_rate(from_currency: str, to_currency: str, new_rate: float):
    from app.core.db import get_session  # Adjust path as needed
    db_session: Session = get_session()

    rate = db_session.query(ExchangeRate).filter(
        ExchangeRate.from_currency == from_currency,
        ExchangeRate.to_currency == to_currency,
    ).first()

    if not rate:
        rate = ExchangeRate(
            from_currency=from_currency,
            to_currency=to_currency,
            rate=new_rate,
        )
        db_session.add(rate)
    else:
        rate.rate = new_rate

    db_session.commit()
