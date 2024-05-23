from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from uuid import uuid4
import random

from src.game_session.database import GameSession, GameUser
from src.core import Core
from src.game_session.game_core import GameCore
router = APIRouter(
    tags=["game_session"],
    prefix="/game_session"
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)

    def disconnect(self, websocket: WebSocket, session_id: str):
        self.active_connections[session_id].remove(websocket)
        if not self.active_connections[session_id]:
            del self.active_connections[session_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, session_id: str):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_text()
            if data.startswith("join"):
                player_name = data.split(":")[1]
                new_player = await GameCore.join_game_session(session_id, player_name)
                await manager.broadcast(f"Player {player_name} joined the game.", session_id)

                game_session = await GameCore.update_game_status_if_ready(session_id)
                if game_session.status == "active":
                    await manager.broadcast(f"Game started!", session_id)
            elif data.startswith("roll"):
                player_id = data.split(":")[1]
                roll_result, updated_player = await GameCore.roll_dice_and_update_position(session_id, player_id)
                await manager.broadcast(f"Player {player_id} rolled {roll_result} and moved to position {updated_player.position}.", session_id)
            else:
                await manager.broadcast(f"Message text was: {data}", session_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
        await manager.broadcast(f"Player disconnected", session_id)