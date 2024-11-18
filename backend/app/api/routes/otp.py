from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from sqlmodel import Session, select
from app.api.deps import get_db
from app.models import OTP, User
from app.helpers.otp_helper import generate_otp, verify_otp
from app.services.twilio_service import send_otp_via_twilio
import uuid

router = APIRouter()

# Time in seconds before an OTP can be resent
RESEND_TIMEOUT = 120  # 2 minutes

@router.post("/generate/{user_id}", dependencies=[Depends(RateLimiter(times=3, seconds=60))], status_code=status.HTTP_201_CREATED)
def generate_otp_endpoint(user_id: str, session: Session = Depends(get_db)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Check if a recent OTP was generated
    otp_record = session.exec(select(OTP).where(OTP.user_id == user_id).order_by(OTP.created_at.desc())).first()
    if otp_record and (datetime.utcnow() - otp_record.created_at).total_seconds() < RESEND_TIMEOUT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Please wait {RESEND_TIMEOUT // 60} minutes before requesting a new OTP."
        )

    # Generate and send OTP
    otp_code = generate_otp(user, session)
    send_otp_via_twilio(user, otp_code)

    # Store OTP in database with expiration
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    otp = OTP(otp_code=otp_code, expires_at=expires_at, user_id=user_id)
    session.add(otp)
    session.commit()
    session.refresh(otp)
    
    return {"message": "OTP sent successfully"}

@router.post("/resend/{user_id}", dependencies=[Depends(RateLimiter(times=3, seconds=60))], status_code=status.HTTP_200_OK)
def resend_otp_endpoint(user_id: str, session: Session = Depends(get_db)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Check if the OTP can be resent
    otp_record = session.exec(select(OTP).where(OTP.user_id == user_id).order_by(OTP.created_at.desc())).first()
    if otp_record and (datetime.utcnow() - otp_record.created_at).total_seconds() < RESEND_TIMEOUT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Please wait {RESEND_TIMEOUT // 60} minutes before resending OTP."
        )

    # Resend the last OTP or generate a new one
    otp_code = otp_record.otp_code if otp_record and otp_record.expires_at > datetime.utcnow() else generate_otp(user, session)
    send_otp_via_twilio(user, otp_code)

    if not otp_record or otp_record.expires_at <= datetime.utcnow():
        # Create a new OTP record if the previous OTP has expired
        expires_at = datetime.utcnow() + timedelta(minutes=10)
        otp = OTP(otp_code=otp_code, expires_at=expires_at, user_id=user_id)
        session.add(otp)
        session.commit()
        session.refresh(otp)
    
    return {"message": "OTP resent successfully"}

@router.post("/resend/{user_id}", status_code=status.HTTP_200_OK)
def resend_otp(user_id: uuid.UUID, session: Session = Depends(get_db)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Check the resend timeout for OTP
    otp_record = session.exec(select(OTP).where(OTP.user_id == user_id).order_by(OTP.created_at.desc())).first()
    if otp_record and (datetime.utcnow() - otp_record.created_at).total_seconds() < RESEND_TIMEOUT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Please wait {RESEND_TIMEOUT // 60} minutes before resending OTP."
        )

    # Reuse or generate a new OTP if the previous has expired
    otp_code = otp_record.otp_code if otp_record and otp_record.expires_at > datetime.utcnow() else generate_otp(user, session)
    send_otp_via_twilio(user, otp_code)

    if not otp_record or otp_record.expires_at <= datetime.utcnow():
        # Create new OTP record if expired
        expires_at = datetime.utcnow() + timedelta(minutes=10)
        otp = OTP(otp_code=otp_code, expires_at=expires_at, user_id=user_id)
        session.add(otp)
        session.commit()
        session.refresh(otp)
    
    return {"message": "OTP has been resent successfully"}