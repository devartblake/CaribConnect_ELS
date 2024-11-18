from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy import JSON
from sqlmodel import SQLModel, Field, Relationship

class CustomizationInfo(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    notes_desc: Optional[str] = None
    show_right_panel: Optional[bool] = False
    bc_view: Optional[bool] = False
    show_home: bool = True
    show_detail_view: bool = True
    unpin_recent_item: Optional[bool] = False    
    theme_id: int = Field(default=None, foreign_key="theme.id")
    user_id: int = Field(default=None, foreign_key="user.id")
    
    # Relationship back to User
    user: Optional["User"] = Relationship(back_populates="customize_info")
    
class CustomizationInfoCreate(SQLModel):
    notes_desc: Optional[str] = None
    show_right_panel: Optional[bool] = None
    bc_view: Optional[bool] = None
    show_home: Optional[bool] = None
    show_detail_view: Optional[bool] = None
    unpin_recent_item: Optional[bool] = None
    theme_id: Optional[uuid.UUID] = None
    user_id: uuid.UUID  # Required when creating

class CustomizationInfoUpdate(SQLModel):
    notes_desc: Optional[str] = None
    show_right_panel: Optional[bool] = None
    bc_view: Optional[bool] = None
    show_home: Optional[bool] = None
    show_detail_view: Optional[bool] = None
    unpin_recent_item: Optional[bool] = None
    theme_id: Optional[uuid.UUID] = None