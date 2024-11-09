import random
from datetime import datetime, timedelta
from sqlmodel import Session
from app.models import User

def generate_otp(user: User, session: Session) -> str:
    otp_code = str(random.randint(100000, 999999))
    otp_created_at = datetime.utcnow()
    otp_expires_at = otp_created_at + timedelta(minutes=3)
    
    user.otp_code = otp_code
    user.otp_created_at = otp_created_at
    user.otp_expires_at = otp_expires_at
    user.otp_attempts = 0
    
    session.add(user)
    session.commit()
    
    return otp_code

def verify_otp(user: User, otp_code: str, session: Session) -> bool:
    if not user.otp_code or datetime.utcnow() > user.otp_expires_at:
        return False

    if user.otp_code == otp_code:
        user.reset_otp()
        session.commit()
        return True
    else:
        user.otp_attempts += 1
        if user.otp_attempts >= 5:
            user.reset_otp()
        session.commit()
        return False
    