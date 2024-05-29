from sqlalchemy import and_, select

from src.database import session_factory
from src.models import Player, GameSession, Board, Propertie
from src.player.utils import PlayerUtils
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

    @staticmethod
    async def update_improvement(session_id: int, index: int, increase: bool):
        async with session_factory() as session:
            async with session.begin():
                result = await session.execute(
                    select(Board)
                    .filter((Board.game_session_id == session_id))
                    .filter(Board.property_id == index)
                )

                game_field = result.scalars().first()

                if game_field.owner_id is None:
                    raise ValueError(f"Field with id '{index}' does not have an owner.")

                if game_field.type != 'prop':
                    if game_field.type != 'special':
                        pass
                    else:
                        raise ValueError(f"Field with id '{index}' is not a property.")

                hotels = game_field.hotel_level
                if hotels == 0 and increase == False:
                    raise ValueError(f"hotel_level of field with id '{index}' is already 0.")
                if hotels == 5 and increase == True:
                    raise ValueError(f"hotel_level {index} is max.")

                if increase:
                    game_field.hotel_level += 1
                else:
                    game_field.hotel_level -= 1

                print(game_field.hotel_level)

            await session.commit()
            await session.refresh(game_field)

    @staticmethod
    async def update_mortgage(session_id: int, index: int, mortgage: bool):
        async with session_factory() as session:
            async with session.begin():
                result = await session.execute(
                    select(Board)
                    .filter((Board.game_session_id == session_id))
                    .filter(Board.property_id == index)
                )

                game_field = result.scalars().first()

                if game_field.owner_id is None:
                    raise ValueError(f"Field with id '{index}' does not have an owner.")

                if game_field.type != 'prop':
                    if game_field.type != 'special':
                        pass
                    else:
                        raise ValueError(f"Field with id '{index}' is not a property.")

                hotels = game_field.hotel_level

                if hotels != 0 and mortgage == True:
                    raise ValueError(f"Need destroy hotels.")

                game_field.mortgage = mortgage

            await session.commit()
            await session.refresh(game_field)

    @staticmethod
    async def update_position(session_id: str, player_id: str, new_position: int):
        return await PlayerUtils.update_player_attribute(session_id, player_id, 'position', new_position % 10)

