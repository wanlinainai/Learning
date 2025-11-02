from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List

router = APIRouter()

class LoginParam(BaseModel):
    username: str
    age: int


@router.get("/test")
async def home(req: Request):
    return {"name": "李白"}

"""
登录：Post请求
"""
@router.post("/login", summary="登录接口")
def login(requestParam: LoginParam):
    return requestParam