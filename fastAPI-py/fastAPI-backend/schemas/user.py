from typing import Optional, List

from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=6)
    user_phone: Optional[str] = Field(default=None, pattern="^1[34567890]\\d{9}$")
    user_status: Optional[bool]
    remarks: Optional[str]
    roles: Optional[List[int]]