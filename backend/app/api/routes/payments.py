from typing import List
import uuid
from fastapi import APIRouter, HTTPException, Depends
from app.services.payment_service import PaymentService
from app.models import PaymentStatus
from sqlalchemy.orm import Session

from app.schemas.paymentSchema import PaymentRequestSchema, PaymentResponseSchema, RefundRequestSchema, RefundResponseSchema
from app.api.deps import get_db

router = APIRouter()
payment_service = PaymentService()

@router.post("/payment/", response_model=PaymentResponseSchema)
def create_payment(payment_data: PaymentRequestSchema, db: Session = Depends(get_db)):
    service = PaymentService(db)
    payment = service.create_payment(payment_data)
    return payment

@router.get("/payment/{payment_id}", response_model=PaymentResponseSchema)
def get_payment(payment_id: uuid.UUID, db: Session = Depends(get_db)):
    service = PaymentService(db)
    payment = service.get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found.")
    return payment

@router.get("/payment_lists", response_model=List[PaymentResponseSchema])
def list_payments(db: Session = Depends(get_db)):
    service = PaymentService(db)
    return service.list_payments()

@router.post("/refunds", response_model=RefundResponseSchema)
def refund_payment(refund_data: RefundRequestSchema, db: Session = Depends(get_db)):
    service = PaymentService(db)
    refund = service.refund_payment(refund_data)
    return refund

# Webhooks for payment services
@router.post("/webhooks/paypal")
async def handle_paypal_webhook(webhook_data: dict):
    # Extract data and update payment status
    transaction_id = webhook_data.get("transaction_id")
    status = PaymentStatus.SETTLED if webhook_data.get("status") == "COMPLETED" else PaymentStatus.FAILED
    payment = payment_service.update_payment_status(transaction_id, status)
    if payment:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Payment not found")

@router.post("/webhooks/stripe")
async def handle_stripe_webhook(webhook_data: dict):
    # Similar to PayPal, handle Stripe events here
    pass