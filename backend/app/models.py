import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union

from pydantic import EmailStr
from sqlalchemy import JSON
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)

# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)

class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)

class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)

# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    user_roles: list["UserRole"] = Relationship(back_populates="user", cascade_delete=True)
    addresses: list["UserAddress"] = Relationship(back_populates="user", cascade_delete=True)
    payments: list["Payment"] = Relationship(back_populates="user", cascade_delete=True)
    page_views: list["PageView"] = Relationship(back_populates="user", cascade_delete=True)
    social_connections: list["SocialConnection"] = Relationship(back_populates="user", cascade_delete=True)
    posts: list["Post"] = Relationship(back_populates="author", cascade_delete=True)
    comments: list["Comment"] = Relationship(back_populates="user", cascade_delete=True)
    professionals: list["Professional"] = Relationship(back_populates="user") # Relationship to Professional

# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

# New UserAddress Model
class UserAddress(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    address_line_1: str = Field(max_length=255)
    address_line_2: str | None = Field(default=None, max_length=255)
    city: str = Field(max_length=255)
    state: str = Field(max_length=255)
    country: str = Field(max_length=255)
    postal_code: str = Field(max_length=20)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)

    # Relationship back to User
    user: User = Relationship(back_populates="addresses")

# User Role-based Access Control (RBAC)
class UserRole(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    role: str = Field(max_length=50) # 'staff', 'client', 'professional'
    sub_role: str | None = Field(max_length=50, default=None) # Optional for further sub-credentials
    user: User = Relationship(back_populates="user_roles")

# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)

# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass

# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore

# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")

# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID

class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int

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
    SAMSUNG_PAY = "samsunng_pay"
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
    address: UserAddress
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
    user: User | None = Relationship(back_populates="payments")

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

# Generic message
class Message(SQLModel):
    message: str

# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None

class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)

# Define an Enum for record types or report categories if needed
class RecordType(str, Enum):
    TYPE_A = "Type A"
    TYPE_B = "Type B"

# Define the Record model
class Record(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    record_type: RecordType
    created_at: datetime = Field(default_factory=datetime.utcnow)
    data: str | None = Field(default=None, max_length=255)

# Social Media account connections
class SocialConnection(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    provider: str  # e.g., "facebook", "google"
    provider_user_id: str  # ID from the social media platform
    access_token: str  # OAuth token for the social media platform
    refresh_token: str | None = None
    expires_in: int | None = None
    user: User | None = Relationship(back_populates="social_connections")

# Page View Model
class PageView(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    url: str = Field(max_length=255)
    # ip_address: IPvAnyAddress | None = None
    user_agent: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    # Relationships
    user: User = Relationship(back_populates="page_views") # Assuming there's a User model

# Post Model
class Post(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    author_id: uuid.UUID = Field(foreign_key="user.id")
    author: User = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post")

# Comment Model
class Comment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    post_id: uuid.UUID = Field(foreign_key="post.id")
    user: User = Relationship(back_populates="comments")
    post: Post = Relationship(back_populates="comments")

# Professional & Service Models
class Service(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    professional_id: int | None = Field(foreign_key="professional.id")
    professionals: "Professional" = Relationship(back_populates="services")

class Professional(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    profession: str = Field(max_length=255, index=True, nullable=False)
    description: str | None = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)
    experience_years: int | None = Field(default=None)
    # Foreign key to the User model
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # Use SQLAlchemy's Column with onupdate
    updated_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))

    # Relationship back to User
    user: "User" = Relationship(back_populates="professionals")
    # Relationships back to Services
    services: list["Service"] = Relationship(back_populates="professionals")

# Define the GeoIP model components (like City, Country, etc.)
class ASN(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    autonomous_system_number: int | None
    autonomous_system_organization: str | None
    ip_address: str | None
    network: str | None = None

    # Relationship with IPAddress
    ip_addresses: list["IPAddress"] = Relationship(back_populates="asn")

class City(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    geoname_id: int | None
    confidence: int | None
    name: str | None
    names: dict[str, Any] | None = Field(sa_column=Column(JSON))

    # Relationship with IPAddress
    ip_addresses: list["IPAddress"] = Relationship(back_populates="city")

class Continent(SQLModel):
    geoname_id: int | None
    code: str | None
    name: str | None
    names: dict[str, Any] | None

class Country(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    geoname_id: int | None
    confidence: str | None
    is_in_european_union: bool | None
    iso_code: str | None
    name: str | None
    names: dict[str, Any] | None = Field(sa_column=Column(JSON))

    # Relationship with IPAddress
    ip_addresses: list["IPAddress"] = Relationship(back_populates="country")

class Location(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    accuracy_radius: int | None
    latitude: float | None
    longitude: float | None
    metro_code: int | None
    time_zone: str | None

    # Relationship with IPAddress
    ip_addresses: list["IPAddress"] = Relationship(back_populates="location")

class Traits(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ip_addresses: list["IPAddress"] = Relationship(back_populates="traits")
    network: str | None = None

class Postal(SQLModel):
    confidence: int | None
    code: str | None

class GeoLocation(SQLModel):
    continent: Continent | None
    country: Country | None
    city: City | None
    location: Location | None
    asn: ASN | None
    postal: Postal | None

# Define the IPAddress model
class IPAddress(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ip_address: str = Field(max_length=45)  # Store IP as a string

    # Relationships to GeoIP models
    city_id: int | None = Field(default=None, foreign_key="city.id")
    city: City | None = Relationship(back_populates="ip_addresses")

    country_id: int | None = Field(default=None, foreign_key="country.id")
    country: Country | None = Relationship(back_populates="ip_addresses")
    asn_id: int | None = Field(default=None, foreign_key="asn.id")
    asn: ASN | None = Relationship(back_populates="ip_addresses")
    location_id: int | None = Field(default=None, foreign_key="location.id")
    location: Location | None = Relationship(back_populates="ip_addresses")
    # Example relationships to other models like GeoIP
    geoip_id: int | None = Field(default=None, foreign_key="geoip.id")
    geoip: Optional["GeoIP"] = Relationship(back_populates="ip_addresses")

    traits_id: int | None = Field(default=None, foreign_key="traits.id")
    traits: Optional["Traits"] = Relationship(back_populates="ip_addresses")

class IPAddressBase(SQLModel):
    ip: str

class IPAddressCreate(IPAddressBase):
    pass

class IPAddressUpdate(SQLModel):
    ip: str | None = None

class GeoIP(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ip_addresses: list["IPAddress"] = Relationship(back_populates="geoip")
