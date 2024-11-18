import uuid
from sqlalchemy import JSON
from sqlmodel import SQLModel, Column,  Field
from typing import Optional

class Theme(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    normal_tab: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    selected_tab: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    new_background: Optional[str] = None
    background: Optional[str] = None
    screen: Optional[str] = None
    type: Optional[str] = None
    
class ThemeCreate(SQLModel):
    normal_tab: Optional[str] = None
    selected_tab: Optional[str] = None
    new_background: Optional[str] = None
    background: Optional[str] = None
    screen: Optional[str] = None
    type: Optional[str] = None

class ThemeUpdate(SQLModel):
    normal_tab: Optional[str] = None
    selected_tab: Optional[str] = None
    new_background: Optional[str] = None
    background: Optional[str] = None
    screen: Optional[str] = None
    type: Optional[str] = None
    