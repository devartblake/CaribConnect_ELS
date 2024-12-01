import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings

logger = logging.getLogger(__name__)

def send_email(to_email, subject, body):
    """
    Sends an email to the specified recipient.
    """
    from_email = settings.EMAILS_FROM_EMAIL  # Email address to send from
    password = settings.SMTP_PASSWORD  # SMTP password
    smtp_server = settings.SMTP_SERVER  # Configure SMTP server in settings
    smtp_port = settings.SMTP_PORT  # Configure SMTP port in settings

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the email server and send the message
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(from_email, password)  # Login to the SMTP server
            server.send_message(msg)  # Send the email
            logger.info(f"Email sent to {to_email} with subject '{subject}'.")
    except smtplib.SMTPException as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
