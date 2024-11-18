import uuid
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlmodel import Session, select

from app.models import Payment, PaymentStatus
from app.services.payment_service import PaymentService
from app.schemas.paymentSchema import PaymentRequestSchema, PaymentResponseSchema, RefundRequestSchema, RefundResponseSchema
from app.api.deps import get_db

router = APIRouter()
payment_service = PaymentService()

@router.post("/", response_model=PaymentResponseSchema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=3, seconds=60))])
def create_payment(payment_data: PaymentRequestSchema, session: Session = Depends(get_db)):
    service = PaymentService(session)
    payment = service.create_payment(payment_data)
    return payment

@router.get("/{payment_id}", response_model=PaymentResponseSchema)
def get_payment(payment_id: uuid.UUID, session: Session = Depends(get_db)):
    service = PaymentService(session)
    payment = service.get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found.")
    return payment

@router.get("/payment_lists", response_model=List[PaymentResponseSchema])
def list_payments(session: Session = Depends(get_db)):
    service = PaymentService(session)
    return service.list_payments()

@router.post("/refunds", response_model=RefundResponseSchema, dependencies=[Depends(RateLimiter(times=3, seconds=60))])
def refund_payment(refund_data: RefundRequestSchema, session: Session = Depends(get_db)):
    service = PaymentService(session)
    refund = service.refund_payment(refund_data)
    return refund

# Webhooks for payment services
@router.post("/webhooks/paypal", dependencies=[Depends(RateLimiter(times= 10, seconds=60))])
async def handle_paypal_webhook(webhook_data: dict, session: Session = Depends(get_db)):
    # Extract data and update payment status
    transaction_id = webhook_data.get("transaction_id")
    status = PaymentStatus.COMPLETED if webhook_data.get("status") == "COMPLETED" else PaymentStatus.FAILED
    payment = payment_service.update_payment_status(transaction_id, status)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found.")
    payment.payment_statux = status
    session.add(payment)
    session.commit()
    return {"status": "success"}

@router.post("/webhooks/stripe", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def handle_stripe_webhook(webhook_data: dict, session: Session = Depends(get_db)):
    transaction_id = webhook_data.get("transaction_id")
    status = PaymentStatus.COMPLETED if webhook_data.get("status") == "succeeded" else PaymentStatus.FAILED
    payment = session.exec(select(Payment).where(Payment.transaction_id == transaction_id)).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found.")
    payment.payment_status = status
    session.add(payment)
    session.commit()
    return {"status": "success"}