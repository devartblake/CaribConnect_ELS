from twilio.rest import Client
from typing import ClassVar
from pydantic import BaseModel
from app.models import User
from app.core.config import settings

class TwilioServiceConfig(BaseModel):
    TWILIO_ACCOUNT_SID: ClassVar[str] = settings.TWILIO_ACCOUNT_SID
    TWILIO_AUTH_TOKEN: ClassVar[str]  = settings.TWILIO_AUTH_TOKEN
    TWILIO_PHONE_NUMBER: ClassVar[str]  = settings.TWILIO_PHONE_NUMBER

client = Client(
    TwilioServiceConfig.TWILIO_ACCOUNT_SID, 
    TwilioServiceConfig.TWILIO_AUTH_TOKEN
)

def send_otp_via_twilio(user: User, otp_code: str):
    """
    Sends an OTP to the user's phone number via Twilio. 
    If the phone number is not available, attempts to send it to an email.
    """
    if user.phone:
        message = client.messages.create(
            body=f"Your OTP code is {otp_code}",
            from_=TwilioServiceConfig.TWILIO_PHONE_NUMBER,
            to=user.phone
        )
        print(f"Message sent: SID={message.sid}")  # Optional debug log
    elif user.email:
        # Placeholder for sending OTP via email (implement this separately)
        pass
    else:
        raise ValueError("User must have either a phone number or email to receive an OTP.")
