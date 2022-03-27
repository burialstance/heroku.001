from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from fastapi.templating import Jinja2Templates

from fastapi.responses import HTMLResponse

# from app.users import current_active_user
from app.coinglass import get_data

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def web_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
