from datetime import datetime
import uuid
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional

class Profile(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    display_label: str = Field(max_length=100)
    name: str = Field(max_length=100, index=True)
    description: str = Field(default=None, max_length=500)
    created_time: datetime = Field(default_factory=datetime.utcnow)  # Ensure defaults
    modified_time: datetime = Field(default_factory=datetime.utcnow)  # Ensure defaults
    
    # Foreign keys
    created_by_user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")
    modified_by_user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")

    # Relationships
    created_by: Optional["User"] = Relationship(sa_relationship_kwargs={"primaryjoin": "Profile.created_by_user_id == User.id","foreign_keys": "Profile.created_by_user_id"})
    modified_by: Optional["User"] = Relationship(sa_relationship_kwargs={"primaryjoin": "Profile.modified_by_user_id == User.id", "foreign_keys": "Profile.modified_by_user_id"})
    