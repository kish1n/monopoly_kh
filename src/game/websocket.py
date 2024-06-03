from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.responses import HTMLResponse

from src.utils.templates import templates
from src.game.utils import GameUtils

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_session_data(self, websocket: WebSocket, session_id: int):
        session_data = await GameUtils.get_sesion_data(session_id)
        session_data_dict = {
            "properties": [prop.dict() for prop in session_data["properties"]],
            "players": [player.dict() for player in session_data["players"]]
        }
        await websocket.send_json(session_data_dict)
        

manager = ConnectionManager()

clients = {}

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: int):
    await manager.connect(websocket)
    await manager.send_session_data(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(f"Session {session_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.get("/session/{session_id}", response_class=HTMLResponse)
async def get_session_page(request: Request, session_id: int):
    return templates.TemplateResponse("session.html", {"request": request, "session_id": session_id})