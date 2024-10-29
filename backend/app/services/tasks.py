import logging
import time
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.helpers.task_helpers import (
    check_system_health,
    cleanup_old_records_db,
    clear_cache,
    create_backup,
    fetch_api_data,
    generate_report_db,
    update_cache,
)
from app.models import Notification, Record, User
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
def send_notification_task(user_id: int, message: str):
    with SessionLocal() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"User {user_id} not found for notification")
            return {"status": "user_not_found", "user_id": user_id}

        try:
            notification = Notification(user_id=user.id, message=message)
            db.add(notification)
            db.commit()
            db.refresh(notification)
            send_message("notifications", message)
            logger.info(f"Notification sent to user {user_id}: {message}")
            return {"status": "notification_sent", "user_id": user_id, "message": message}
        except Exception as e:
            db.rollback()
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
