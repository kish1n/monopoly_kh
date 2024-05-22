from fastapi import HTTPException, Depends
from sqlalchemy import and_, asc, desc, func, Integer, cast, update
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert


from src.database import session_factory, engine, Base
from src.game_session.database import GameUser, GameSession
from src.auth.models import User
from src.auth.base_config import current_user


class Core:
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()

    @staticmethod
    async def create_game_session():
        async with session_factory() as session:
            async with session.begin():
                new_game_session = GameSession(
                    status="waiting",
                    current_player_index=0,
                    max_players=4,
                    current_players_count=0
                )
                session.add(new_game_session)
                await session.flush()
            await session.commit()

            return new_game_session.id

    @staticmethod
    async def join_game_session(session_id: str, name: str):
        async with session_factory() as session:
            async with session.begin():
                game_session = select(GameSession).filter(GameSession.id == session_id)
                game_session = await session.execute(game_session)
                game_session = game_session.scalars().one_or_none()

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

                return new_game_user


