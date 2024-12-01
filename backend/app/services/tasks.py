import logging
import time
from datetime import datetime, timedelta

from bson import ObjectId
from celery import shared_task

from app.core.db import SessionLocal, get_database_session, mongodb_db
from app.helpers.task_helpers import (
    check_system_health,
    cleanup_old_records_db,
    clear_cache,
    create_backup,
    fetch_api_data,
    generate_report_db,
    update_cache,
)
from app.models import Record
from app.services.exchange_rate_service import ExchangeRateService
from app.services.notification_service import NotificationService
from app.workers.celery_worker import celery_worker

from .email_service import send_email  # Assumes you have an email service
from .message_queue import send_message

logger = logging.getLogger(__name__)

@celery_worker.task
def process_payment(payment_id: int, amount: float, user_id: int):
    try:
        time.sleep(5)  # Simulate a long-running task
        # Implement your payment processing logic here
        logger.info(f"Processed payment with ID: {payment_id} for user {user_id} with amount {amount}")
        return {"status": "success", "payment_id": payment_id, "amount": amount}
    except Exception as e:
        logger.error(f"Error processing payment {payment_id}: {e}")
        return {"status": "failed", "error": str(e)}

@celery_worker.task
def refund_payment(payment_id: int, amount: float):
    try:
        logger.info(f"Refunding payment {payment_id} for amount {amount}")
        return {"status": "refunded", "payment_id": payment_id, "amount": amount}
    except Exception as e:
        logger.error(f"Error refunding payment {payment_id}: {e}")
        return {"status": "failed", "error": str(e)}

@celery_worker.task
def send_email_task(email: str, subject: str, body: str):
    try:
        send_email(email, subject, body)
        logger.info(f"Sent email to {email} with subject '{subject}'")
        return {"status": "email_sent", "email": email}
    except Exception as e:
        logger.error(f"Error sending email to {email}: {e}")
        return {"status": "failed", "error": str(e)}

@celery_worker.task
def send_notification_task(user_id: str, message: str):
    """
    Send a notification to a user and store it in MongoDB.

    Args:
        user_id (str): The ID of the user to send the notification to.
        message (str): The message content for the notification.

    Returns:
        dict: A result dictionary indicating the task status.
    """
    # Initialize the NotificationService
    notification_service = NotificationService(db=mongodb_db)

    try:
        # Create a new notification for the user
        notification_id = notification_service.create_notification(
            user_id=ObjectId(user_id),  # Convert user_id to MongoDB ObjectId
            type="system",  # Example notification type
            content=message,
        )
        logger.info(f"Notification created for user {user_id}: {message}")

        # Simulate sending the notification (e.g., via WebSocket, Email, etc.)
        send_message("notifications", message)
        logger.info(f"Notification sent to user {user_id}: {message}")

        return {"status": "notification_sent", "user_id": user_id, "message": message, "notification_id": notification_id}

    except Exception as e:
        logger.error(f"Error sending notification to user {user_id}: {e}")
        return {"status": "failed", "error": str(e)}

@celery_worker.task
def generate_report(report_id: int):
    try:
        time.sleep(10)  # Simulate a long-running task
        logger.info(f"Generated report with ID: {report_id}")
        return {"status": "report_generated", "report_id": report_id}
    except Exception as e:
        logger.error(f"Error generating report {report_id}: {e}")
        return {"status": "failed", "error": str(e)}

@celery_worker.task
def cleanup_old_records():
    logger.info("Starting cleanup of old records...")
    try:
        cutoff_date = datetime.now() - timedelta(days=30)
        records_deleted = cleanup_old_records_db(cutoff_date)
        logger.info(f"Deleted {records_deleted} old records from the database.")
    except Exception as e:
        logger.error(f"Error during cleanup of old records: {e}")
    logger.info("Finished cleanup of old records.")

@celery_worker.task
def backup_database():
    try:
        create_backup()
        logger.info("Database backup completed.")
    except Exception as e:
        logger.error(f"Error during database backup: {e}")

@celery_worker.task
def refresh_cache():
    try:
        clear_cache()
        update_cache()
        logger.info("Cache refreshed successfully.")
    except Exception as e:
        logger.error(f"Error refreshing cache: {e}")

@celery_worker.task
def generate_daily_report():
    logger.info("Generating daily report...")
    try:
        report = generate_report_db()
        send_email("admin@example.com", "Daily Report", report)
        logger.info("Daily report generated and sent to admin via email.")
    except Exception as e:
        logger.error(f"Error generating daily report: {e}")
    logger.info("Finished generating daily report.")

@celery_worker.task
def heartbeat_check():
    logger.info("Performing heartbeat check...")
    try:
        is_healthy = check_system_health()
        if is_healthy:
            logger.info("System is healthy.")
        else:
            logger.warning("System health check failed!")
    except Exception as e:
        logger.error(f"Error during heartbeat check: {e}")
    logger.info("Finished heartbeat check.")

@celery_worker.task
def poll_external_api():
    api_url = 'https://api-m.sandbox.paypal.com'
    data = fetch_api_data(api_url)
    with SessionLocal() as db:
        try:
            record = Record(
                action="API Poll",
                description="Fetched data successfully" if data else "Failed to fetch data",
                status="Success" if data else "Failure"
            )
            db.add(record)
            db.commit()
            logger.info(f"API poll logged with status: {'Success' if data else 'Failure'}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error logging API poll: {e}")
            return {"status": "failed", "error": str(e)}
        return {"status": "success"}

@shared_task(name="tasks.update_exchange_rates_task")
def update_exchange_rates_task():
    """
    Celery task to update exchange rates in the database.
    """
    db_session = next(get_database_session())
    try:
        exchange_rate_service = ExchangeRateService(db_session=db_session, celery_app=celery_worker)
        exchange_rate_service.update_exchange_rates()
    finally:
        db_session.close()
