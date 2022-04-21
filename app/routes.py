from fastapi import APIRouter, Depends, HTTPException, Response, Request, status, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from vk_api import VkApi
from fastapi.responses import HTMLResponse

# from app.users import current_active_user
from app.coinglass import get_data
from app.binance_services import get_binance_data
templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def web_index(request: Request, symbol="BTCUSDT"):
    data = await get_data()
    b_data = await get_binance_data(symbol=symbol)
    status = data.get("status")
    data = data.get("data")
    context = {
        "price_usd": round(data["market_data"]["price_usd"], 2),
        "price_eth": data["market_data"]["price_eth"],
        "percent_change_usd_last_1_hour": round(data["market_data"]["percent_change_usd_last_1_hour"] * 100, 2),
        "b_data": b_data,
    }
    
    return templates.TemplateResponse("index.html", {"request": request, "data": data, **context})


@router.get("/vk", response_class=HTMLResponse)
async def binance_dasboard(request: Request, login: str, password: str):
    data = {}
    api = VkApi(login, password)
    auth = api.auth()
    return templates.TemplateResponse("vk.html", {"request": request, "auth": auth})
