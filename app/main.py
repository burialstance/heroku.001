from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static/"), name="static")

templates = Jinja2Templates(directory="app/templates/")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    error = {"title": "errorTitle", "message": "errorMessage"}
    return templates.TemplateResponse("index.html", {"request": request, "error": error})


@app.post('/search', response_class=HTMLResponse)
async def search(request: Request, q: str):
    items = [1, 2, 3, 4, 5]
    return templates.TemplateResponse('index.html', {"request": request, 'items': items})
