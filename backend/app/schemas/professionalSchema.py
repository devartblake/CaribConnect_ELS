from pydantic import BaseModel, Field, UUID4, constr
from typing import Optional
from datetime import datetime

class ProfessionalBaseSchema(BaseModel):
    name: str = Field(..., max_length=255)
    profession: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    is_active: bool = True
    experience_years: Optional[int] = None

class ProfessionalCreateSchema(ProfessionalBaseSchema):
    user_id: UUID4

class ProfessionalUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    profession: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None
    experience_years: Optional[int] = None

class ProfessionalResponseSchema(ProfessionalBaseSchema):
    id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
