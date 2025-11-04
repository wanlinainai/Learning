from datetime import datetime
from tkinter import OptionMenu
from typing import Optional, List

from pydantic import BaseModel, Field, validator

from schemas.base import ResAntTable, BaseResp


class CreateUser(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=6, max_length=12)
    user_phone: Optional[str] = Field(default=None, pattern="^1[34567890]\\d{9}$")
    user_status: Optional[bool]
    remarks: Optional[str]
    roles: Optional[List[int]]

class UpdateUser(BaseModel):
    id: int
    username: Optional[str] = Field(min_length=3, max_length=20)
    password: Optional[str] = Field(min_length=6, max_length=12)
    user_phone: Optional[str] = Field(regex="^1[34567890]\\d{9}$")
    user_status: Optional[bool]
    remarks: Optional[str]

class UserListItem(BaseModel):
    key: int
    id: int
    username: str
    age: Optional[int]
    user_type: bool
    nickname: Optional[str]
    user_phone: Optional[str]
    user_email: Optional[str]
    full_name: Optional[str]
    user_status: bool
    header_status: Optional[str]
    sex: int
    remarks: Optional[str]
    create_time: datetime
    update_time: datetime

class UserListData(ResAntTable):
    data: List[UserListItem]

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

class UserInfo(BaseModel):
    username: str
    age: Optional[int]
    user_type: bool
    nickname: Optional[str]
    user_phone: Optional[str]
    user_email: Optional[str]
    full_name: Optional[str]
    scopes: Optional[List[str]]
    user_status: bool
    header_img: Optional[str]
    sex: int

class CurrentUser(BaseResp):
    data: UserInfo

class UpdateUserInfo(BaseModel):
    nickname: Optional[str]
    user_email: Optional[str]
    header_img: Optional[str]
    user_phone: Optional[str] = Field(regex="^1[34567890]\\d{9}$", description="手机号")
    password: Optional[str] = Field(min_length=6, max_length=12, description="密码")

    # 将空字符串转换成None
    @validator("*")
    def blank_strings(cls, v):
        if v == "":
            return None
        return v