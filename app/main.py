import random
import aiohttp
import asyncio
from fastapi import FastAPI, Request, Form, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.coinglass import get_data
app = FastAPI(debug=True)

app.mount("/static", StaticFiles(directory="app/static/"), name="static")

templates = Jinja2Templates(directory="app/templates/")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, coin: str = "btc"):
    error = None
    items = (await get_data(coin=coin))[::-1]
    coins = {
        "current": coin,
        "all": [
            "BTC",
            "ETH", 
            "PEOPLE",
        ],
    }
    context = {
        "coins": coins,
        "request": request,
        "error": error,
        "items": items,
        "long": round(items[0].longAccount * 100, 3),
        "short": round(items[0].shortAccount  * 100, 3),
    }
    return templates.TemplateResponse("index.html", context)


@app.get('/search', response_class=HTMLResponse)
async def search(request: Request, query: str):
    items = [f"{i} {query}" for i in range(20)]
    context = {
        'request': request,
        'items': items,
        'query': query
    }
    return templates.TemplateResponse('index.html', context)

async def get(url):
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as response:
            status_code = response.status
            return {k: str(getattr(response, k)) for k in dir(response)}

@app.get('/ip/{host}')
async def fetch_ip(request: Request, host: str):
    r = await get(f"http://{host}")
    context = {
        **r,
        
    }
    return context


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
