import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union

from pydantic import IPvAnyAddress
from sqlalchemy import JSON
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

# Social Media account connections
class SocialConnection(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    provider: str  # e.g., "facebook", "google"
    provider_user_id: str  # ID from the social media platform
    access_token: str  # OAuth token for the social media platform
    refresh_token: str | None = None
    expires_in: int | None = None
    user: "User" = Relationship(back_populates="social_connections")

# Page View Model
class PageView(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    url: str = Field(max_length=255)
    # ip_address: "IPvAnyAddress" = Relationship(back_populates="ip_addresses")
    user_agent: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    # Relationships
    user: "User" = Relationship(back_populates="page_views") # Assuming there's a User model

# Post Model
class Post(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    author_id: uuid.UUID = Field(foreign_key="user.id")
    author: "User" = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post")

# Comment Model
class Comment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    post_id: uuid.UUID = Field(foreign_key="post.id")
    user: "User" = Relationship(back_populates="comments")
    post: Post = Relationship(back_populates="comments")
