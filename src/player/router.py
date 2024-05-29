from fastapi import APIRouter, HTTPException

from src.core import Core
from src.game.core import GameCore
from src.player.core import PlayerCore

router = APIRouter(
    tags=["player"],
    prefix="/game/player"
)

@router.put("/{session_id}/update_improvement")
async def update_improvement(session_id: int, index: int, increase: bool):
    try:
        possessions_state = await PlayerCore.update_improvement(session_id=session_id, index=index, increase=increase)
        return possessions_state
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{session_id}/update_mortgage")
async def update_mortgage(session_id: int, index: int, mortgage: bool):
    try:
        possessions_state = await PlayerCore.update_mortgage(session_id=session_id, index=index, mortgage=mortgage)
        return possessions_state
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{session_id}/update_position")
async def update_position(session_id: int, player_id: int, position: int):
    try:
        await PlayerCore.update_position(session_id=session_id, player_id=player_id, new_position=position)
        return {"status": "ok"}
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