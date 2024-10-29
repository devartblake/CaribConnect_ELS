import random
import time
from pathlib import Path

from celery import Celery
from celery.utils.log import get_task_logger
from fastapi_mail import (  # Use FastAPI Mail for sending
    ConnectionConfig,
    FastMail,
    MessageSchema,
)
from jinja2 import Environment, FileSystemLoader
from mjml import mjml2html  # For MJML to HTML conversion

# Configure Celery
celery = Celery(
    "tasks",
    broker="amqp://guest:guest@rabbitmq:5672//",
    backend="redis://redis:6379/0",
)

celery_log = get_task_logger(__name__)

# Define the template folder path
TEMPLATES_DIR = Path(__file__).resolve().parent / "email-templates"

# Set up Jinja2 environment to load templates
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# Example configuration for FastMail (you'll need to adapt this with your credentials)
conf = ConnectionConfig(
    MAIL_USERNAME="your-email@example.com",
    MAIL_PASSWORD="your-password",
    MAIL_FROM="your-email@example.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.mailtrap.io",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
)

@celery.task
def send_email(email: str, template_name: str, context: dict):
    # Simulate processing time
    time.sleep(random.randint(1, 4))
    
    # Load and render the template
    template = env.get_template(f"{template_name}.html")
    html_content = template.render(context)

    # If using MJML template
    # mjml_template = env.get_template(f"{template_name}.mjml")
    # mjml_content = mjml_template.render(context)
    # html_content = mjml2html(mjml_content)["html"]

    # Define email message
    message = MessageSchema(
        subject="Test Email",
        recipients=[email],  # List of recipients
        body=html_content,
        subtype="html"
    )

    # Send email using FastMail
    fast_mail = FastMail(conf)
    fast_mail.send_message(message)
    
    celery_log.info("Email has been sent to %s", email)
    return {"msg": f"Email has been sent to {email}", "details": {"destination": email, }, }

# Example: send_email.delay("user@example.com", "welcome_template", {"username": "John Doe"})