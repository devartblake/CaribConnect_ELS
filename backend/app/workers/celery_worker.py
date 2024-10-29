import os
from jinja2 import Environment, FileSystemLoader
from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue

# Configure Celery
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbit-mq:5672/")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery_worker = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["app.services.tasks"]
)

celery_worker.conf.update(
    result_expires=3600,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    task_default_queue='default',
    task_default_exchange='default',
    task_default_routing_key='default'
)

# Configure Queues
celery_worker.conf.task_queues = (
    Queue('default', Exchange('default', type='direct'), routing_key='default'),
    Queue('payment_queue', Exchange('payment_exchange', type='direct'), routing_key='payment'),
    Queue('notification_queue', Exchange('notification_exchange', type='fanout'), routing_key=''),
)

# Initialize Jinja2 environment
env = Environment(loader=FileSystemLoader("app/templates/emails"))

def render_template(template_name, **kwargs):
    template = env.get_template(template_name)
    return template.render(**kwargs)

# Example task that uses a template
@celery_worker.task
def send_email_notification(email_type, recipient, **kwargs):
    # Choose the template based on the email_type
    template_mapping = {
        "welcome": "welcome.html",
        "reminder": "reminder.html",
        "report": "report.html",
        "record": "record.html",
        "notification": "notification.html",
    }
    
    # Render the chosen template
    template_name = template_mapping.get(email_type, "notification.html")
    email_content = render_template(template_name, **kwargs)
    
    # Example email sending function (you'll need to replace this with actual email-sending logic)
    print(f"Sending email to {recipient}")
    print("Content:")
    print(email_content)

# Define the beat schedule
celery_worker.conf.beat_schedule = {
    'send-email-notifications-every-minute': {
        'task': 'app.services.tasks.send_email_notification',
        'schedule': crontab(),  # Every minute
        'args': ('reminder', 'recipient@example.com', {'name': 'User'}),
    },
    'cleanup-old-records-every-hour': {
        'task': 'app.services.task.cleanup_old_records',
        'schedule': crontab(minute=0, hour=3),  # Every thrree hours
        'args': ('record', 'recipient@example.com', {'name': 'User'}),
    },
    'generate-daily-report-at-midnight': {
        'task': 'app.services.tasks.generate-daily-report',
        'schedule': crontab(minute=0, hour=0),  # Every day at midnight
        'args': ('report', 'recipient@example.com', {'name': 'User'}),
    }
}