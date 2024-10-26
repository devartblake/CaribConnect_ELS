import uuid
from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    IPAddress,
    IPAddressUpdate,
    Item,
    ItemCreate,
    User,
    UserCreate,
    UserUpdate,
)
from app.schemas.ipvSchema import IPAddressCreate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

# Create IP Address
def create_ip_address(session: Session, ip_address_create: IPAddressCreate) -> IPAddress:
    ip_address = IPAddress.from_orm(ip_address_create)
    session.add(ip_address)
    session.commit()
    session.refresh(ip_address)
    return ip_address

# Get IP Address by ID
def get_ip_address_by_id(session: Session, ip_id: int) -> IPAddress | None:
    return session.get(IPAddress, ip_id)

# Get IP Address by IP
def get_ip_address_by_ip(session: Session, ip: str) -> IPAddress | None:
    return session.exec(select(IPAddress).where(IPAddress.ip == ip)).first()

# Get all IP Addresses
def get_all_ip_addresses(session: Session, skip: int = 0, limit: int = 100) -> list[IPAddress]:
    return session.exec(select(IPAddress).offset(skip).limit(limit)).all()

# Update IP Address
def update_ip_address(session: Session, ip_id: int, ip_address_update: IPAddressUpdate) -> IPAddress:
    ip_address = session.get(IPAddress, ip_id)
    if not ip_address:
        return None

    for key, value in ip_address_update.dict(exclude_unset=True).items():
        setattr(ip_address, key, value)

    session.add(ip_address)
    session.commit()
    session.refresh(ip_address)
    return ip_address

# Delete IP Address
def delete_ip_address(session: Session, ip_id: int) -> IPAddress | None:
    ip_address = session.get(IPAddress, ip_id)
    if not ip_address:
        return None

    session.delete(ip_address)
    session.commit()
    return ip_address
