from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from fastapi.templating import Jinja2Templates

# from app.users import current_active_user


templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/")
async def web_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
