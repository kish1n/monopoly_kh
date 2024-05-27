from typing import List, Optional
import os
from functools import partial
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.database import get_session

from src.core import Core
from src.game.game_core import GameCore
from src.game.player_core import PlayerCore
from src.game.database import GameSession, Player
from src.auth.base_config import current_user


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

@router.put("/{session_id}/update_improvement")
async def update_improvement(session_id: int, index: int, increase: bool):
    try:
        possessions_state = await GameCore.update_improvement(session_id=session_id, index=index, increase=increase)
        return possessions_state
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{session_id}/update_mortgage")
async def update_mortgage(session_id: int, index: int, mortgage: bool):
    try:
        possessions_state = await GameCore.update_mortgage(session_id=session_id, index=index, mortgage=mortgage)
        return possessions_state
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{session_id}/update_position")
async def update_position(session_id: int, player_id: int, position: int):
    try:
        await GameCore.update_position(session_id=session_id, player_id=player_id, new_position=position)
        return {"status": "ok"}
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

@router.put("/{session_id}/buy_possesion")
async def buy_possesion(session_id: int, player_id: int, property_id: int):
    try:
        await PlayerCore.buy_possesion(session_id=session_id, player_id=player_id, property_id=property_id)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))