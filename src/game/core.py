from typing import Dict
from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import JSONB

from src.database import session_factory
from src.models import Player, GameSession, Board, Propertie
from src.game.utils import PropertyModel, GamerModel
from src.player.utils import PlayerUtils
from src.player.core import PlayerCore

class GameCore:
    @staticmethod
    async def join_game_session(session_id: str, player_name: str):
        async with session_factory() as session:
            async with session.begin():

                # Проверяем наличие игровой сессии
                result = await session.execute(select(GameSession).filter_by(id=session_id))
                game_session = result.scalars().first()
                if not game_session:
                    raise ValueError(f"Game session with id '{session_id}' does not exist.")

                # Проверяем наличие игрока с таким же user_id в этой сессии
                result = await session.execute(
                    select(Player).filter_by(game_session_id=session_id)
                )
                existing_players = result.scalars().all()
                new_q_value = len(existing_players)

                if (new_q_value + 1) > 4:
                    raise ValueError("Game session is full")
                # Создаем нового игрока и добавляем его в игровую сессию
                new_player = Player(
                    game_session_id=session_id,
                    name=player_name,
                    q=new_q_value
                )
                session.add(new_player)

            await session.commit()  # Коммит после добавления игрока
            await session.refresh(new_player)  # Обновляем сессию для получения ID игрока
            return new_player.id

    @staticmethod
    async def get_possessions_state(session_id: int):
        async with session_factory() as session:
            result = await session.execute(select(GameSession).filter_by(id=session_id))
            game_session = result.scalars().first()
            if not game_session:
                raise ValueError(f"Game session with id '{session_id}' does not exist.")

            return game_session.possessions_state

    @staticmethod
    async def get_players(session_id: int):
        async with session_factory() as session:
            result = await session.execute(
                select(Player).filter(Player.game_session_id == session_id)
            )
            players = result.scalars().all()
            return [
                {
                    "id": player.id,
                    "name": player.name,
                    "balance": player.balance,
                    "q": player.q,
                    "position": player.position
                }
                for player in players
            ]

    @staticmethod
    async def get_sesion_data(session_id: int):
        async with session_factory() as session:

            data_of_session = {
                "properties": [],
                "players": [],
            }

            result = await session.execute(
                select(Player).filter(Player.game_session_id == session_id)
            )

            players = result.scalars().all()

            for player in players:
                data_of_session["players"].append(
                    GamerModel(
                        id=int(player.id),
                        name=player.name,
                        user_id=int(player.user_id) if player.user_id is not None else -1,
                        game_session_id=int(player.game_session_id),
                        q=int(player.q),
                        position=int(player.position),
                        balance=int(player.balance),
                        owned_fields=[]
                    )
                )

            playground = await session.execute(
                select(Board).filter(Board.game_session_id == session_id)
            )

            playground = playground.scalars().all()

            for prop in playground:

                qur_property = await session.execute(
                    select(Propertie).filter(Propertie.id == prop.property_id)
                )
                qur_property = qur_property.scalars().one_or_none()

                data_of_session["properties"].append(
                    PropertyModel(
                        number=int(prop.property_id),
                        name=qur_property.name,
                        type=prop.type,
                        price=int(qur_property.price) if qur_property.price is not None else -1,
                        owner_id=int(prop.owner_id) if prop.owner_id is not None else -1,
                        street_color=qur_property.street_color if qur_property.street_color is not None else "",
                        hotel_level=int(prop.hotel_level) if prop.hotel_level is not None else -1,
                        mortgage=int(prop.mortgage) if prop.mortgage is not None else -1,

                        improvement_value=[],
                        rent_value=[],

                    )
                )

            return data_of_session

    @staticmethod
    async def make_trade(session_id: int, tender_id: int, reciver_id: int, log: JSONB):
        async with session_factory() as session:
            async with session.begin():

                result = await session.execute(
                    select(Player).filter(Player.id == tender_id)
                    .filter(Player.game_session_id == session_id)
                )
                tender = result.scalars().first()

                result = await session.execute(
                    select(Player).filter(Player.id == reciver_id)
                    .filter(Player.game_session_id == session_id)
                )
                reciver = result.scalars().first()

                if not tender or not reciver:
                    raise ValueError("Player not found")

                print(log)


