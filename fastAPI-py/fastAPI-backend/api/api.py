from fastapi import APIRouter

from . import Base
from endpoints import user, role

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(Base.router, tags=["测试接口功能"])
api_router.include_router(user.router, tags=["用户管理"], prefix="/admin")
api_router.include_router(role.router, tags=["角色管理"], prefix="/admin")