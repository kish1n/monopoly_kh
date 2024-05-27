from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.future import select
from src.game.entities.Dice import Dice

from src.database import session_factory
from src.game.database import Player, GameSession, Board, Propertie

class PlayerCore:
    @staticmethod
    async def buy_possesion(session_id: int, player_id: int, property_id: int):
        async with session_factory() as session:
            async with session.begin():

                game_session = await session.execute(select(GameSession).filter_by(id=session_id))
                game_session = game_session.scalars().first()

                if not game_session:
                    raise ValueError(f"Game session with id '{session_id}' does not exist.")

                player = await session.execute(select(Player).filter_by(id=player_id))
                player = player.scalars().first()

                if not player:
                    raise ValueError(f"Player with id '{player_id}' does not exist.")

                board = await session.execute(
                    select(Board).filter_by(game_session_id=session_id, property_id=property_id)
                )
                field = board.scalars().first()

                propertie = await session.execute(select(Propertie).filter_by(id=property_id))
                propertie = propertie.scalars().first()

                if not propertie:
                    raise ValueError(f"Propertie with id '{property_id}' does not exist.")

                if not field:
                    raise ValueError(
                        f"Board with property_id '{property_id}' does not exist in session '{session_id}'.")

                if field.owner_id is not None:
                    raise ValueError(f"Field with property_id '{property_id}' already has an owner.")

                if player.balance < propertie.price:
                    raise ValueError(f"Player with id '{player_id}' does not have enough money.")

                if field.type != 'prop':
                    if field.type != 'special':
                        pass
                    raise ValueError(f"Field with id '{property_id}' is not a property. {field}")

                if player.position != field.property_id:
                    raise ValueError(f"Player with id '{player_id}' is not on field with property_id '{property_id}'.")

                field.owner_id = player_id
                player.balance -= field.property.price

            await session.commit()
            await session.refresh(player)
            await session.refresh(field)
            return player.balance


