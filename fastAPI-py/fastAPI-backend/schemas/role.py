from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from schemas.base import ResAntTable


class CreateRole(BaseModel):
    role_name: str = Field(min_length=3, max_length=10)
    role_status: Optional[bool] = False
    role_desc: Optional[str] = Field(max_length=255)

class UpdateRole(BaseModel):
    id: int
    role_name: str
    role_status: Optional[bool]
    role_desc: Optional[str]


class RoleItem(BaseModel):
    id: int
    key: int
    role_name: str
    role_status: Optional[bool]
    role_desc: Optional[str]
    create_time: datetime
    update_time: datetime

class RoleList(ResAntTable):
    data: List[RoleItem]
