import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, Union

from pydantic import EmailStr
from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel

class Role(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    display_label: str = Field(max_length=100)
    name: str = Field(max_length=100, index=True)
    description: str = Field(default=None, max_length=500)
    share_with_peers: bool = Field(default=False)
    admin_user: bool = Field(default=False)
    forecast_manager_user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")
    reporting_to_user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")

    forecast_manager: Optional["User"] = Relationship(sa_relationship_kwargs={"primaryjoin": "Role.forecast_manager_user_id == User.id"})
    reporting_to: Optional["User"] = Relationship(sa_relationship_kwargs={"primaryjoin": "Role.reporting_to_user_id == User.id"})
    # Relationship to UserRole
    user_roles: list["UserRole"] = Relationship(back_populates="role")
