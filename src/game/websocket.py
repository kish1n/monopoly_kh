from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
import json

from src.game.core import GameCore

router = APIRouter()

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

    async def broadcast(self, message: dict, session_id: str):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                if connection.client_state == WebSocketState.CONNECTED:
                    await connection.send_text(json.dumps(message))

manager = ConnectionManager()

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received data: {data}")
            message = json.loads(data)
            action = message.get("action")

            if action == "join":
                player_name = data.split(":")[2][1:-2]
                await manager.broadcast(
                    {"type": "message", "message": f"Player {player_name} joined the game."},
                    session_id
                )
                await GameCore.join_game_session(session_id, player_name)
                players = await GameCore.get_players(int(session_id))
                print("Player joined the game")
                await manager.broadcast(
                    {"type": "update", "players": players},
                    session_id
                )

            elif action == "roll":
                player_id = action.get("id")
                roll_result, updated_player = await GameCore.roll_dice_and_update_position(session_id, player_id)
                await manager.broadcast({
                    "type": "update",
                    "message": f"Player {player_id} rolled {roll_result} and moved to position {updated_player.position}.",
                    "players": await GameCore.get_players(session_id)
                }, session_id)
            else:
                await manager.broadcast(
                    {"type": "message", "message": f"Message text was: {data}"},
                    session_id
                )

    except WebSocketDisconnect:
        print(f"WebSocket connection closed for session {session_id}")
        await manager.broadcast({"type": "message", "message": "Player disconnected"}, session_id)
    except Exception as e:
        print(f"WebSocket connection error: {e}")
        if websocket.client_state == WebSocketState.CONNECTED:
            print("Sending error message")
