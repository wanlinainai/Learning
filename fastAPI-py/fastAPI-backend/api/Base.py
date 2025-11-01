from fastapi import APIRouter, Request
router = APIRouter()

@router.get("/test")
async def home(req: Request):
    return "fastAPI"