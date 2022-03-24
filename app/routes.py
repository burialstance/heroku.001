from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.users import current_active_user


templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/")
async def web_index():
    return templates.TemplateResponse("item.html", {"request": request})
