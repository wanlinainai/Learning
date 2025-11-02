from typing import Optional, List

from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=6)
    user_phone: Optional[str] = Field(default=None, pattern="^1[34567890]\\d{9}$")
    user_status: Optional[bool]
    remarks: Optional[str]
    roles: Optional[List[int]]

class AccessToken(BaseModel):
    token: Optional[str]
    expire_in: Optional[int]

class UserLogin(BaseModel):
    data: AccessToken

class AccountLogin(BaseModel):
    username: Optional[str] = Field(min_length=3, max_length=20 ,description="用户名")
    password: Optional[str] = Field(min_length=6, max_length=12, description="密码")
    mobile: Optional[str] = Field(regex="^1[34567890]\\d{9}$", description="手机号")
    captcha: Optional[str] = Field(min_length=6, max_length=6, description="验证码")