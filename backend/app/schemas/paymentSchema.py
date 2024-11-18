import re
from pydantic import BaseModel, EmailStr, Field, UUID4, constr, field_validator
from datetime import datetime
from typing import Any, Optional, Union
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
    CASH_APP = "cashapp"
    KLARNA = "klarna"
    LINK = "link"
    PAY_PAL = "pay_pal"
    SAMSUNG_PAY = "samsunng_pay"
    ZIP = "zip"

# Enum for payment status
class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    AUTHORIZED = "authorized"
    SETTLED = "settled"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELED = "canceled"

class CreditCardDetailsSchema(BaseModel):
    card_number: str
    card_brand: str
    expiration_date: str # MM/YYYY
    cvv: str  # 3-4 digits
    
    @field_validator("expiration_date")
    def validate_expiration_date(cls, value):
        if not re.match(r"^(0[1-9]|1[0-2])/(\d{4})$", value):
            raise ValueError("Expiration date must be in MM/YYYY format.")
        return value
    
    @field_validator("cvv")
    def validate_cvv(cls, value):
        # Ensure the value is treated as a string.
        if isinstance(value, int):
            value = str(value)
        # Validate against the regex pattern for 3-4 digits.
        if not re.match(r"^\d{3,4}$", value):
            raise ValueError("CVV must be 3-4 digits.")
        return value

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
    locale: Optional[str]  # Locale, e.g., en_US
    
    @field_validator("locale")
    def validate_locale(cls, value):
        if value and not re.match(r"^[a-z]{2}_[A-Z]{2}$", value):
            raise ValueError("Locale must be in the format en_US.")
        return value
    
    # Polymorphic Payment Method Details
PaymentDetailsSchema = Union[CreditCardDetailsSchema, UsBankAccountSchema, PayPalDetailsSchema]
    
# Payment Request Schema
class PaymentRequestSchema(BaseModel):
    user_id: UUID4
    amount: float = Field(..., gt=0, le=1_000_000)  # Example limit
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")  # ISO 4217 code
    status: PaymentStatus = PaymentStatus.PENDING
    provider: PaymentProvider = Field(default=PaymentProvider.PAYPAL)
    payment_method_nonce: Optional[str] = None  # Provider-specific
    payment_method_type: PaymentMethodType = PaymentMethodType.CREDIT_CARD
    payment_details: Optional[PaymentDetailsSchema]  # Polymorphic details
    metadata: Optional[dict[str, Any]] = None  # For extensibility
    transaction_id: Optional[str]
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
    metadata: Optional[dict[str, str]] = None

# Refund Request Schema
class RefundRequestSchema(BaseModel):
    transaction_id: str  # The ID of the original payment transaction
    amount: Optional[float] = None  # Partial or full refund, if specified
    refund_reason: Optional[str] = None

# Refund Response Schema
class RefundResponseSchema(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    refund_id: Optional[str] = None  # Provider's refund ID
    transaction_id: str
    amount: float
    status: PaymentStatus
    refunded_at: datetime = Field(default_factory=datetime.utcnow)
    refund_reason: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None