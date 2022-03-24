from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.users import current_active_user



router = APIRouter()

@router.get("/")
async def web_index(user = Depends(current_active_user)):
    return user
