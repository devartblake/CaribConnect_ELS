import uuid
from datetime import datetime
from typing import Optional, List

from app.models import Payment, PaymentProvider, PaymentStatus
from app.core.db import SessionLocal
from app.schemas.paymentSchema import PaymentRequestSchema, PaymentResponseSchema, RefundRequestSchema, RefundResponseSchema


class PaymentService:
    def __init__(self):
        self.db = SessionLocal
    
    def create_payment(self, payment_request: PaymentRequestSchema) -> PaymentResponseSchema:
        payment = Payment(
            user_id=payment_request.user_id,
            amount=payment_request.amount,
            currency=payment_request.currency,
            provider=payment_request.provider,
            status=PaymentStatus.PENDING,
            transaction_id=str(uuid.uuid4()),
        )
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return PaymentResponseSchema.from_orm(payment)
    
    def get_payment(self, payment_id: uuid) -> Optional[PaymentResponseSchema]:
        payment = self.db.query(Payment).filter(Payment.id == payment_id).first()
        return PaymentResponseSchema.from_orm(payment) if payment else None

    def list_payments(self) -> List[PaymentResponseSchema]:
        payments = self.db.query(Payment).all()
        return [PaymentResponseSchema.from_orm(payment) for payment in payments]

    def update_payment_status(self, payment_id: uuid.UUID, status: PaymentStatus) -> Optional[Payment]:
        payment = self.get_payment(payment_id)
        if payment:
            payment.status = status
            payment.completed_at = datetime.utcnow() if status == PaymentStatus.SETTLED else None
            self.db.commit()
            self.db.refresh(payment)
        return payment

    def refund_payment(self, refund_data: RefundRequestSchema) -> RefundResponseSchema:
        payment = self.db.query(Payment).filter(Payment.transaction_id == refund_data.transaction_id).first()
        if not payment:
            raise ValueError("Payment not found.")
        
        refund = RefundResponseSchema(
            transaction_id=payment.transaction_id,
            amount=refund_data.amount or payment.amount,
            status=PaymentStatus.SETTLED,
            refunded_at=datetime.utcnow()
        )
        return refund
    
    def process_payment(self, provider: PaymentProvider, amount: float, currency: str):
        if provider == PaymentProvider.STRIPE:
            return self._process_stripe_payment(amount, currency)
        elif provider == PaymentProvider.PAYPAL:
            return self._process_paypal_payment(amount, currency)
        # Add more providers as needed

    def _process_stripe_payment(self, amount, currency):
        # Stripe-specific processing
        pass

    def _process_paypal_payment(self, amount, currency):
        # PayPal-specific processing
        pass