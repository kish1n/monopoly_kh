from fastapi import APIRouter, HTTPException

from src.core import Core
from src.game.core import GameCore
from src.player.core import PlayerCore

router = APIRouter(
    tags=["game"],
    prefix="/game"
)

@router.post("/create")
async def create_game_session():
    try:
        session_id = await Core.create_game_session('test')
        return {"session_id": session_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/join")
async def join_game_session(session_id: int, palyer_name: str):
    try:
        player_id = await GameCore.join_game_session(session_id, palyer_name)
        return {"player_id": player_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{session_id}/get_players")
async def get_players(session_id: int):
    try:
        players = await GameCore.get_players(session_id=session_id)
        return players
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{session_id}/get_session_data")
async def get_session_data(session_id: int):
    try:
        session_data = await GameCore.get_sesion_data(session_id=session_id)
        return session_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{session_id}/make_trade")
async def make_trade(session_id: int, player_id: int, target_player_id: int, amount):
    try:
        await GameCore.make_trade(session_id, player_id, target_player_id, amount)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



