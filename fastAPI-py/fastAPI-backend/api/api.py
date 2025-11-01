from fastapi import APIRouter

from api import Base

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(Base.router, prefix="/test", tags=["测试接口功能"])