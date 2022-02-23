import random
import aiohttp
Import asyncio
from fastapi import FastAPI, Request, Form, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.coinglass import get_data
app = FastAPI(debug=True)

app.mount("/static", StaticFiles(directory="app/static/"), name="static")

templates = Jinja2Templates(directory="app/templates/")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    error = {"title": "errorTitle", "message": "errorMessage"} if random.random() > 0.5 else None
    print(error)
    context = {
        "request": request,
        "error": error,
        "data": await get_data()
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
        data = await get_data()
        asyncio.sleep(1)
        await websocket.send_json({"data": data})
        print(data)
