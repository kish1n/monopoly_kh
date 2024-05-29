from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.future import select

from src.database import session_factory
from src.models import Player, GameSession, Board, Propertie


class PlayerUtils:
    @staticmethod
    async def update_player_attribute(session_id: str, id: str, attribute: str, value):
        async with session_factory() as session:
            async with session.begin():
                result = await session.execute(
                    select(Player).filter(
                        Player.game_session_id == session_id,
                        Player.id == id
                    )
                )
                player = result.scalars().first()
                print(player.position)
                if player:
                    setattr(player, attribute, value)
                else:
                    raise HTTPException(status_code=404, detail="Player not found")
            await session.commit()
            await session.refresh(player)
            return player