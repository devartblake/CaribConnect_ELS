from pydantic import BaseModel, EmailStr, Field, UUID4
from datetime import datetime
from typing import Optional
from enum import Enum
import uuid

# Enum for payment provider
class PaymentProvider(str, Enum):
    PAYPAL = "paypal"
    STRIPE = "stripe"
    VENMO = "venmo"
    CHASE = "chase"

# Enum for payment method type
class PaymentMethodType(str, Enum):
    CREDIT_CARD = "credit_card"
    ACH_DIRECT_DEBIT = "us_bank_account"
    AFFIRM = "affirm"
    ATFER_PAY_CLEAR_PAY = "afterpay_clearpay"
    AMAZON_PAY = "amazon_pay"
    CARD_PRESENT = "card_present"
    CASH_APP_PAY = "cashapp"
    KLARNA = "klarna"
    LINK = "link"
    PAY_PAL = "pay_pal"
    SAMSUNG_PAY = "samsunng_pay"
    ZIP = "zip"

# Enum for payment status
class PaymentStatus(str, Enum):
    PENDING = "pending"
    AUTHORIZED = "authorized"
    SETTLED = "settled"
    FAILED = "failed"
    REFUNDED = "refunded"

class CreditCardDetailsSchema(BaseModel):
    card_number: str
    card_brand: str
    expiration_date: str
    cvv: str

class UsBankAccountSchema(BaseModel):
    account_holder_type: str
    account_type: str
    bank_name: str
    fingerprint: str
    last4: str
    routing_number: str

class PayPalDetailsSchema(BaseModel):
    paypal_id: str

class BillingDetailsSchema(BaseModel):
    address: Optional[str]
    email: Optional[EmailStr]
    name: Optional[str]
    phone: Optional[str]
    
# Payment Request Schema
class PaymentRequestSchema(BaseModel):
    user_id: UUID4
    amount: float = Field(..., gt=0)
    currency: str = "USD"
    status: PaymentStatus
    provider: PaymentProvider = Field(default=PaymentProvider.PAYPAL)
    payment_method_nonce: Optional[str] = None  # Braintree-specific
    payment_method_type: PaymentMethodType = PaymentMethodType.CREDIT_CARD
    transaction_id: str
    settled_at: Optional[datetime]
    customer_id: Optional[UUID4] = None
    order_id: Optional[str] = None
    device_data: Optional[str] = None  # For fraud prevention if required by provider

# Payment Response Schema
class PaymentResponseSchema(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    user_id: UUID4
    amount: float
    currency: str
    provider: PaymentProvider
    status: PaymentStatus
    transaction_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

# Refund Request Schema
class RefundRequestSchema(BaseModel):
    transaction_id: str  # The ID of the original payment transaction
    amount: Optional[float] = None  # Partial or full refund, if specified

# Refund Response Schema
class RefundResponseSchema(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    transaction_id: str
    amount: float
    status: PaymentStatus
    refunded_at: datetime = Field(default_factory=datetime.utcnow)