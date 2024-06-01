from fastapi import APIRouter, HTTPException
from typing import List

from src.core import Core
from src.game.utils import GameUtils

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

@router.put("/{session_id}/make_trade")
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


@router.patch("/{session_id}/update_position")
async def update_position(session_id: int, player_id: int, position: int):
    try:
        await GameUtils.update_position(session_id=session_id, player_id=player_id, new_position=position)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/buy_possesion")
async def buy_possesion(session_id: int, player_id: int, property_id: int):
    try:
        await GameUtils.buy_possesion(session_id=session_id, player_id=player_id, property_id=property_id)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/{player_id}/get_posession")
async def get_posession(session_id: int, player_id: int, property_id: int):
    try:
        possessions = await GameUtils.change_owner_posession(session_id=session_id, player_id=player_id, property_id=property_id)
        return possessions
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/sell_possession")
async def sell_possession(session_id: int, player_id: int, property_id: int):
    try:
        await GameUtils.sell_possession(session_id=session_id, player_id=player_id, property_id=property_id)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/update_improvement")
async def update_improvement(session_id: int, property_id: int, increase: bool):
    try:
        possessions_state = await GameUtils.update_improvement(session_id=session_id, property_id=property_id, increase=increase)
        return possessions_state
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/update_mortgage")
async def update_mortgage(session_id: int, property_id: int, mortgage: bool):
    try:
        possessions_state = await GameUtils.update_mortgage(session_id=session_id, property_id=property_id, mortgage=mortgage)
        return possessions_state
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/{player_id}/update_part_balance")
async def update_part_of_balance(session_id: int, player_id: int, delta_balance: int):
    try:
        await GameUtils.update_part_balance(session_id=session_id, player_id=player_id, delta_balance=delta_balance)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{session_id}/{player_id}/update_balance")
async def update_balance(session_id: int, player_id: int, new_balance: int):
    try:
        await GameUtils.update_balance(session_id=session_id, player_id=player_id, new_balance=new_balance)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))