from sqlmodel import Session
from app.models import User
from app.helpers.otp_helper import verify_otp, generate_otp

def test_generate_otp(session: Session, test_user: User):
    otp_code = generate_otp(test_user, session)
    assert otp_code.isdigit() and len(otp_code) == 6

def test_verify_otp(session: Session, test_user: User):
    otp_code = generate_otp(test_user, session)
    assert verify_otp(test_user, otp_code, session) is True
    assert test_user.otp_code is None  # Ensure OTP is reset

def test_invalid_otp(session: Session, test_user: User):
    generate_otp(test_user, session)
    assert not verify_otp(test_user, "123456", session)
    