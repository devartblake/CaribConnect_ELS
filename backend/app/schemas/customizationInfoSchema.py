from typing import Optional
from sqlmodel import SQLModel, Field
import uuid

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
