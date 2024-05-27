from fastapi import HTTPException, Depends
from sqlalchemy import and_, asc, desc, func, Integer, cast, update
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert


from src.database import session_factory, engine, Base
from src.game.database import Player, GameSession, Board, Propertie, possessions_state

class Core:
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            tables_to_create_and_drop = [
                GameSession.__table__,
                Player.__table__,
                Board.__table__,
                #Propertie.__table__
            ]
            await conn.run_sync(Base.metadata.drop_all, tables=tables_to_create_and_drop)
            await conn.run_sync(Base.metadata.create_all, tables=tables_to_create_and_drop)
            await conn.commit()

    @staticmethod
    async def create_game_session(name: str):
        async with session_factory() as session:
            # Проверяем наличие сессии с таким же именем
            new_game_session = GameSession(
                name=name,
                is_active=True
            )

            session.add(new_game_session)
            await session.commit()  # Коммит после добавления сессии
            await session.refresh(new_game_session)  # Обновляем сессию для получения ID

        async with session_factory() as session:
            for i in range(1, 10):
                field = await session.execute(select(Propertie).filter_by(id=i))
                res = field.scalars().first()
                new_board = Board(
                    game_session_id=new_game_session.id,
                    type=res.type,
                    property_id=res.id,
                )
                session.add(new_board)

            await session.commit()
            await session.refresh(new_board)

            return new_game_session.id