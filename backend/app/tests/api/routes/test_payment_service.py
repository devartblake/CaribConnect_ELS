import uuid
from datetime import datetime
from app.services.payment_service import PaymentService
from app.models import PaymentRequest, PaymentProvider, RefundRequest, PaymentStatus

payment_service = PaymentService()

def test_create_payment():
    request = PaymentRequest(
        user_id=uuid.uuid4(),
        amount=100.0,
        currency="USD",
        provider=PaymentProvider.STRIPE,
        payment_method_nonce="sample_nonce"
    )
    payment = payment_service.create_payment(request)
    assert payment.amount == 100.0
    assert payment.status == PaymentStatus.PENDING

def test_refund_payment():
    request = PaymentRequest(
        user_id=uuid.uuid4(),
        amount=50.0,
        currency="USD",
        provider=PaymentProvider.PAYPAL,
        payment_method_nonce="sample_nonce"
    )
    payment = payment_service.create_payment(request)

    refund_request = RefundRequest(transaction_id=payment.transaction_id, amount=50.0)
    refunded_payment = payment_service.refund_payment(refund_request)
    assert refunded_payment.status == PaymentStatus.REFUNDED
    assert refunded_payment.amount == -50.0
