import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union

from pydantic import EmailStr
from sqlalchemy import JSON
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

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
    owner: "User" = Relationship(back_populates="items")

# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID

class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int