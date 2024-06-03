from fastapi import APIRouter, HTTPException, Request
from typing import List

from src.core import Core
from src.data.utils import DataGetter
from src.game.utils import GameUtils
from src.utils.templates import templates

router = APIRouter(
    tags=["methods"],
    prefix="/game/actions"
)

'''GET METHODS'''

@router.patch("/{session_id}/{player_id}/get_posession", tags=["getters"])
async def get_posession(session_id: int, player_id: int, property_id: int):
    try:
        possessions = await GameUtils.change_owner_posession(session_id=session_id, player_id=player_id, property_id=property_id)
        return possessions
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

'''SETTER METHODS'''

@router.patch("/{session_id}/{player_id}/set_position", tags=["setters"])
async def set_position(session_id: int, player_id: int, position: int):
    try:
        await GameUtils.set_position(session_id=session_id, player_id=player_id, new_position=position)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/{property_id}/set_mortgage", tags=["setters"])
async def set_mortgage(session_id: int, property_id: int, mortgage: bool):
    try:
        possessions_state = await GameUtils.set_mortgage(session_id=session_id, property_id=property_id,
                                                            mortgage=mortgage)
        return possessions_state
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/{player_id}/set_balance", tags=["setters"])
async def set_balance(session_id: int, player_id: int, new_balance: int):
    try:
        await GameUtils.set_balance(session_id=session_id, player_id=player_id, new_balance=new_balance)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/{player_id}/set_prisson", tags=["setters"])
async def set_prisson(session_id: int, player_id: int, status: bool):
    try:
        status = await GameUtils.set_prisson(session_id=session_id, player_id=player_id, status=status)
        return {"status": status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

'''UPDATE METHODS'''

@router.patch("/{session_id}/{player_id}/update_part_balance", tags=["updaters"])
async def update_part_of_balance(session_id: int, player_id: int, delta_balance: int):
    try:
        await GameUtils.update_part_balance(session_id=session_id, player_id=player_id, delta_balance=delta_balance)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/{player_id}/update_improvement", tags=["updaters"])
async def update_improvement(session_id: int, property_id: int, increase: bool):
    try:
        possessions_state = await GameUtils.update_improvement(session_id=session_id, property_id=property_id,
                                                               increase=increase)
        return possessions_state
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/{player_id}/update_prisson", tags=["updaters"])
async def update_prisson(session_id: int, player_id: int):
    try:
        status = await GameUtils.set_prisson(session_id=session_id, player_id=player_id)
        return {"status": status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

'''MAKE TRADE METHODS'''

@router.put("/{session_id}/make_trade/{sender_player_id}/{target_player_id}", tags=["trade"])
async def make_trade(session_id: int,
                     sender_player_id: int, sender_amount: int, sender_properties: List[str],
                     target_player_id: int, target_amount: int, target_properties: List[str]):
    try:
        await GameUtils.make_trade(
            session_id=session_id,
            sender_player_id=sender_player_id, sender_amount=sender_amount, sender_properties=sender_properties,
            target_player_id=target_player_id, target_amount=target_amount, target_properties=target_properties
        )
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

'''ACTIONS METHODS'''

@router.patch("/{session_id}/{player_id}/buy_possesion", tags=["actions"])
async def buy_possesion(session_id: int, player_id: int, property_id: int):
    try:
        await GameUtils.buy_possesion(session_id=session_id, player_id=player_id, property_id=property_id)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/{player_id}/sell_possession", tags=["actions"])
async def sell_possession(session_id: int, player_id: int, property_id: int):
    try:
        await GameUtils.sell_possession(session_id=session_id, player_id=player_id, property_id=property_id)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{session_id}/{player_id}/prisson", tags=["actions"])
async def go_to_prisson(session_id: int, player_id: int):
    try:
        status = await GameUtils.checker_prisson(session_id=session_id, player_id=player_id)
        return {"status": status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

