from pydantic import BaseModel
from typing import Optional
import uuid

class ThemeBase(BaseModel):
    normal_tab: Optional[dict]
    selected_tab: Optional[dict]
    new_background: Optional[str]
    background: Optional[str]
    screen: Optional[str]
    type: Optional[str]

class ThemeCreate(ThemeBase):
    pass

class ThemeUpdate(BaseModel):
    normal_tab: Optional[dict]
    selected_tab: Optional[dict]
    new_background: Optional[str]
    background: Optional[str]
    screen: Optional[str]
    type: Optional[str]

class ThemeRead(ThemeBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
        