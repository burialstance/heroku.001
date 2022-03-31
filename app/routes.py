from fastapi import APIRouter, Depends, HTTPException, Response, Request, status, WebSocket, WebSocketDisconnect
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
        "percent_change_usd_last_1_hour": round(data["market_data"]["percent_change_usd_last_1_hour"] * 100, 2),
    }
    
    return templates.TemplateResponse("index.html", {"request": request, "data": data, **context})


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await get_data()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
