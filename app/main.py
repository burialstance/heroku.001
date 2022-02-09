import random
import aiohttp
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(debug=True)

app.mount("/static", StaticFiles(directory="app/static/"), name="static")

templates = Jinja2Templates(directory="app/templates/")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    error = {"title": "errorTitle", "message": "errorMessage"} if random.random() > 0.5 else None
    print(error)
    context = {
        "request": request,
        "error": error
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
