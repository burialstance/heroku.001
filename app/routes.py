from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from fastapi.templating import Jinja2Templates

from fastapi.responses import HTMLResponse

# from app.users import current_active_user
from app.coinglass import get_data

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def web_index(request: Request):
    data = await get_data()
    status = data.get("status")
    data = data.get("data")
    context = {
        "price_usd": round(data["market_data"]["price_usd"], 2),
        "price_eth": data["market_data"]["price_eth"],
        "percent_change_usd_last_1_hour": round(data["market_data"]["percent_change_usd_last_1_hour"], 3),
        
    }
    
    return templates.TemplateResponse("index.html", {"request": request, "data": data, **context})
