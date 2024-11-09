from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from sqlmodel import Session
from app.core.db import get_database_session
from app.models import User
from app.helpers.otp_helper import generate_otp, verify_otp
from app.services.twilio_service import send_otp_via_twilio

router = APIRouter()

@router.post("/otp/generate", dependencies=[Depends(RateLimiter(times=3, seconds=60))], status_code=status.HTTP_201_CREATED)
def generate_otp_endpoint(user_id: str, session: Session = Depends(get_database_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    otp_code = generate_otp(user, session)
    send_otp_via_twilio(user, otp_code)
    return {"message": "OTP sent successfully"}

@router.post("/otp/verify", dependencies=[Depends(RateLimiter(times=5, seconds=60))], status_code=status.HTTP_200_OK)
def verify_otp_endpoint(user_id: str, otp_code: str, session: Session = Depends(get_database_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if verify_otp(user, otp_code, session):
        return {"message": "OTP verified successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")
