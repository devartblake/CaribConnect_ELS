import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Union

from pydantic import EmailStr
from sqlalchemy import JSON
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

# Payments status enum
class PaymentStatus(str, Enum):
    PENDING = "pending"
    AUTHORIZED = "authorized"
    SETTLED = "settled"
    FAILED = "failed"

# Payment Method Type enum
class PaymentMethodType(str, Enum):
    CREDIT_CARD = "credit_card"
    AFFIRM = "affirm"
    ATFER_PAY_CLEAR_PAY = "afterpay_clearpay"
    AMAZON_PAY = "amazon_pay"
    CARD_PRESENT = "card_present"
    CASH_APP_PAY = "cashapp"
    KLARNA = "klarna"
    LINK = "link"
    PAY_PAL = "pay_pal"
    SAMSUNG_PAY = "samsung_pay"
    ACH_DIRECT_DEBIT = "us_bank_account"
    ZIP = "zip"

# Payment provide enum
class PaymentProvider(str, Enum):
    PAYPAL = "paypal"
    STRIPE = "stripe"
    VENMO = "venmo"

# Credit card  brands
class CreditCardBrands(str, Enum):
    AMEX = "amex"
    DISCOVER = "discover"
    MASTERCARD = "mastercard"
    VISA = "visa"
    UNKNOWN = "unknown"

# Billing information
class BillingDetails(SQLModel):
    address: "UserAddress" = Relationship(back_populates="user")
    email: EmailStr | None = Field(default=None, max_length=255)
    name:  str | None
    phone: str | None

class UsBankAccount(SQLModel):
    account_holder_type: str
    account_type: str
    bank_name: str
    financial_connections_account: str | None
    fingerprint: str
    last4: str
    networks: dict[str, Any]
    routing_number: str
    status_detailss: dict[str, Any]

# Payment sub attributes
class CreditCardDetials(SQLModel):
    card_number: str = Field(..., min_length=13, max_length=19)  # Typical length range for card numbers
    card_brand: CreditCardBrands = CreditCardBrands.UNKNOWN
    expiration_date: str  # Format MM/YY
    cvv: str = Field(..., min_length=3, max_length=4)  # Typically 3 or 4 digits
    
class BankTransferDetails(SQLModel):
    routing_number: str = Field(..., min_length=9, max_length=9)  # Standard 9-digit format
    account_number: str

class PayPalDetails(SQLModel):
    paypal_id: str  # PayPal account ID
    
# Payments model
class Payment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    amount: float = Field(gt=0)  # Greater than 0
    currency: str = Field(default="USD")
    provider: PaymentProvider = Field(default=PaymentProvider.PAYPAL)
    status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    transaction_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None
    user: "User" = Relationship(back_populates="payments")

# Payment Request Model
class PaymentRequest(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    amount: float = Field(gt=0)
    currency: str = Field(default="USD")
    payment_method_nonce: str  # For Braintree's unique payment method identifier
    payment_method_type: PaymentMethodType = PaymentMethodType.CREDIT_CARD
    payment_details: Union[CreditCardDetials, BankTransferDetails, PayPalDetails]
    provider: PaymentProvider = PaymentProvider.PAYPAL
    customer_id: uuid.UUID | None = None
    order_id: str | None = None
    device_data: str | None = None  # Optional device data for fraud prevention

    class Config:
        use_enum_values = True
        
# Payment Response Model
class PaymentResponse(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    amount: float
    currency: str
    status: PaymentStatus
    provider: PaymentProvider
    transaction_id: str  # Braintree transaction ID
    created_at: datetime = Field(default_factory=datetime.utcnow)
    settled_at: datetime | None = None
    customer_id: uuid.UUID | None = None
    order_id: str | None = None

# Refund Models
class RefundRequest(SQLModel):
    transaction_id: str  # Braintree transaction ID for the original payment
    amount: float | None = None  # Optional, refund the full amount if not specified

class RefundResponse(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    transaction_id: str  # The transaction ID that was refunded
    amount: float
    status: PaymentStatus
    refunded_at: datetime = Field(default_factory=datetime.utcnow)
