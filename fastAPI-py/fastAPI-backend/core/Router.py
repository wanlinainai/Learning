from fastapi import APIRouter

from api.api import api_router

router = APIRouter()

# API路由
router.include_router(api_router)