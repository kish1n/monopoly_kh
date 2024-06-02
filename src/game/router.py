from fastapi import APIRouter, HTTPException, Request
from typing import List

from src.core import Core
from src.game.utils import GameUtils
from src.utils.templates import templates

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
        player_id = await GameUtils.join_game_session(session_id, palyer_name)
        return {"player_id": player_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{session_id}/get_players")
async def get_players(session_id: int):
    try:
        players = await GameUtils.get_players(session_id=session_id)
        return players
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{session_id}/get_session_data")
async def get_session_data(session_id: int):
    try:
        session_data = await GameUtils.get_sesion_data(session_id=session_id)
        return session_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))