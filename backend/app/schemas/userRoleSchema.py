from typing import Optional
from pydantic import BaseModel, Field
import uuid

# Role-based access control (RBAC) schema
class UserRoleBase(BaseModel):
    role: str = Field(..., max_length=50)
    sub_role: Optional[str] = Field(None, max_length=50)

class UserRoleCreate(UserRoleBase):
    pass

class UserRoleUpdate(UserRoleBase):
    role: Optional[str] = Field(None, max_length=50)

class UserRolePublic(UserRoleBase):
    id: uuid.UUID
