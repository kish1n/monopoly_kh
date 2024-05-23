from fastapi import HTTPException, Depends
from sqlalchemy import and_, asc, desc, func, Integer, cast, update
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from game.entities.Dice import Dice

from src.database import session_factory, engine, Base
from src.game_session.database import GameUser, GameSession
from src.auth.models import User
from src.auth.base_config import current_user

class GameCore:
    @staticmethod
    async def join_game_session(session_id: str, name: str):
        async with session_factory() as session:
            async with session.begin():
                result = await session.execute(
                    select(GameSession).filter(GameSession.id == session_id)
                )
                game_session = result.scalars().first()
                if not game_session:
                    raise HTTPException(status_code=404, detail="Game session not found")

                if game_session.current_players_count >= game_session.max_players:
                    raise HTTPException(status_code=400, detail="Game session is full")

                new_game_user = GameUser(
                    name=name,
                    money=1500,
                    position=game_session.current_players_count,
                    in_jail=0,
                    session_id=game_session.id
                )

                session.add(new_game_user)
                game_session.current_players_count += 1
                await session.commit()

                # Проверка и обновление статуса игры
                await GameCore.update_game_status_if_ready(session_id)

                return new_game_user

    @staticmethod
    async def update_game_status_if_ready(session_id: str):
        async with session_factory() as session:
            async with session.begin():
                result = await session.execute(
                    select(GameSession).filter(GameSession.id == session_id)
                )
                game_session = result.scalars().first()
                if game_session:
                    if game_session.current_players_count >= game_session.max_players:
                        game_session.status = "active"
                        await session.commit()
                        return game_session
                    else:
                        return game_session
                else:
                    raise HTTPException(status_code=404, detail="Game session not found")

    @staticmethod
    async def update_player_attribute(session_id: str, player_id: str, attribute: str, value):
        async with session_factory() as session:
            async with session.begin():
                result = await session.execute(
                    select(GameUser).filter(
                        GameUser.session_id == session_id,
                        GameUser.user_id == player_id
                    )
                )
                player = result.scalars().first()
                if player:
                    setattr(player, attribute, value)
                    await session.commit()
                    await session.refresh(player)
                    return player
                else:
                    raise HTTPException(status_code=404, detail="Player not found")

    @staticmethod
    async def update_players_money(session_id: str, player_id: str, difference: int):
        async with session_factory() as session:
            async with session.begin():
                result = await session.execute(
                    select(GameUser).filter(
                        GameUser.session_id == session_id,
                        GameUser.user_id == player_id
                    )
                )
                player = result.scalars().first()
                if player:
                    player.money += difference
                    await session.commit()
                    await session.refresh(player)
                    return player
                else:
                    raise HTTPException(status_code=404, detail="Player not found")

    @staticmethod
    async def update_player_queue(session_id: str, player_id: str, new_queue: int):
        # Call the universal update function
        return await GameCore.update_player_attribute(session_id, player_id, 'queue', new_queue)

    @staticmethod
    async def update_player_position(session_id: str, player_id: str, new_position: int):
        # Call the universal update function
        return await GameCore.update_player_attribute(session_id, player_id, 'position', new_position % 40)

    @staticmethod
    async def roll_dice_and_update_position(session_id: str, player_id: str):
        dice = Dice()
        roll_result = dice.roll()

        async with session_factory() as session:
            async with session.begin():
                result = await session.execute(
                    select(GameUser).filter(GameUser.session_id == session_id, GameUser.user_id == player_id)
                )
                player = result.scalars().first()
                if not player:
                    raise HTTPException(status_code=404, detail="Player not found")

                new_position = player.position + sum(roll_result)
                player.position = new_position % 40
                await session.commit()
                await session.refresh(player)

        return roll_result, player

    @staticmethod
    async def update_player_in_jail(session_id: str, player_id: str, in_jail: bool):
        # Call the universal update function
        return await GameCore.update_player_attribute(session_id, player_id, 'in_jail', in_jail)