import random

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

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
