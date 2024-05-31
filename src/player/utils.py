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

    @staticmethod
    async def check_monopoly_for_player(session_id: str, player_id: str, color: str):
        async with session_factory() as session:
            async with session.begin():
                result = await session.execute(
                    select(Player)
                    .filter((Player.game_session_id == session_id))
                    .filter(Player.id == player_id)
                )
                player = result.scalars().one_or_none()

                if player is None:
                    raise HTTPException(status_code=404, detail="Player not found")

                street = await session.execute(
                    select(Propertie)
                    .filter(Propertie.street_color == color)
                )
                fields = street.scalars().all()

                if fields is None:
                    raise HTTPException(status_code=404, detail="Color not found")

                board = await session.execute(
                    select(Board)
                    .filter(Board.game_session_id == session_id)
                    .filter(Board.owner_id == player_id)
                )
                playground = board.scalars().all()

                for i in range(len(playground)):
                    if playground[i].owner_id != player_id:
                        return False
                return True

    @staticmethod
    async def chek_mogage_for_player(session_id: str, player_id: str, property_id: str):
        async with session_factory() as session:
            result = await session.execute(
                select(Player)
                .filter((Player.game_session_id == session_id))
                .filter(Player.id == player_id)
            )
            player = result.scalars().one_or_none()

            if player is None:
                raise HTTPException(status_code=404, detail="Player not found")

            field = await session.execute(
                select(Board)
                .filter(Board.game_session_id == session_id)
                .filter(Board.property_id == property_id)
            )
            field = field.scalars().one_or_none()

            if field is None:
                raise HTTPException(status_code=404, detail="Field not found")

            print(field.owner_id, player_id, field.owner_id == player_id)

            if field.owner_id != player_id:
                raise HTTPException(status_code=400, detail="Player is not an owner of this field")

            if field.mortgage == 1:
                return 1

            return 0


