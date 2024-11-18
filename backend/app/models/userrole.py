import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, Union

from pydantic import EmailStr
from sqlalchemy import JSON
from sqlmodel import Column, Field, Relationship, SQLModel

# User Role-based Access Control (RBAC)
class UserRole(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    role_id: uuid.UUID = Field(foreign_key="role.id", nullable=False)  # 'staff', 'client', 'professional'
    permissions: Optional[str] = Field(default=None)
    reporting_to: Optional[str] = Field(default=None)
    sub_role: Optional[str] = Field(max_length=50, default=None)
    
    # Relationships
    user: list["User"] = Relationship(back_populates="user_roles")
    role: list["Role"] = Relationship(back_populates="user_roles")
