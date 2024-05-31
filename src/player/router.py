from fastapi import APIRouter, HTTPException

from src.core import Core
from src.game.core import GameCore
from src.player.core import PlayerCore
from src.player.utils import PlayerUtils

router = APIRouter(
    tags=["action"],
    prefix="/game/action"
)

@router.patch("/{session_id}/update_position")
async def update_position(session_id: int, player_id: int, position: int):
    try:
        await PlayerCore.update_position(session_id=session_id, player_id=player_id, new_position=position)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/buy_possesion")
async def buy_possesion(session_id: int, player_id: int, property_id: int):
    try:
        await PlayerCore.buy_possesion(session_id=session_id, player_id=player_id, property_id=property_id)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/{player_id}/get_posession")
async def get_posession(session_id: int, player_id: int, property_id: int):
    try:
        possessions = await PlayerCore.change_owner_posession(session_id=session_id, player_id=player_id, property_id=property_id)
        return possessions
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/sell_possession")
async def sell_possession(session_id: int, player_id: int, property_id: int):
    try:
        await PlayerCore.sell_possession(session_id=session_id, player_id=player_id, property_id=property_id)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/update_improvement")
async def update_improvement(session_id: int, property_id: int, increase: bool):
    try:
        possessions_state = await PlayerCore.update_improvement(session_id=session_id, property_id=property_id, increase=increase)
        return possessions_state
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/update_mortgage")
async def update_mortgage(session_id: int, property_id: int, mortgage: bool):
    try:
        possessions_state = await PlayerCore.update_mortgage(session_id=session_id, property_id=property_id, mortgage=mortgage)
        return possessions_state
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/{player_id}/update_part_balance")
async def update_part_of_balance(session_id: int, player_id: int, delta_balance: int):
    try:
        await PlayerCore.update_part_balance(session_id=session_id, player_id=player_id, delta_balance=delta_balance)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/{player_id}/update_balance")
async def update_balance(session_id: int, player_id: int, new_balance: int):
    try:
        await PlayerCore.update_balance(session_id=session_id, player_id=player_id, new_balance=new_balance)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))