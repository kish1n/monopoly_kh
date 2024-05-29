from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.future import select

from src.database import session_factory
from src.models import Player, GameSession


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
