from fastapi import APIRouter, Request
router = APIRouter()

@router.get("/")
async def home(req: Request):
    return "fastAPI"