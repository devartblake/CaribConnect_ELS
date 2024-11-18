from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class RoleBase(BaseModel):
    display_label: str
    name: str
    description: Optional[str]
    share_with_peers: Optional[bool] = False
    admin_user: Optional[bool] = False

class RoleCreateSchema(RoleBase):
    forecast_manager_user_id: Optional[uuid.UUID]
    reporting_to_user_id: Optional[uuid.UUID]

# Properties to receive via API on creation
class RoleReadSchema(RoleBase):
    id: uuid.UUID

# Properties to receive via API on update
class RoleUpdateSchema(RoleBase):
    forecast_manager_user_id: Optional[uuid.UUID]
    reporting_to_user_id: Optional[uuid.UUID]

# Properties to return via API
class RolePublic(RoleBase):
    id: uuid.UUID
    