from sqlalchemy import and_, select
from fastapi import HTTPException

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

                if propertie.price is None:
                    raise ValueError(f"Field with id '{property_id}' is not a property. {field.property_id}")

                if int(player.balance) < int(propertie.price):
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
    async def sell_possession(session_id: str, player_id: str, property_id: str):
        async with session_factory() as session:
            async with session.begin():
                result = await session.execute(
                    select(Board)
                    .filter((Board.game_session_id == session_id))
                    .filter(Board.property_id == property_id)
                )

                game_field = result.scalars().first()

                if game_field.owner_id is None:
                    raise ValueError(f"Field with id '{property_id}' does not have an owner.")

                if game_field.owner_id != player_id:
                    raise ValueError(f"Player with id '{player_id}' is not an owner of field with id '{property_id}'.")

                if game_field.type != 'prop':
                    if game_field.type != 'special':
                        pass
                    else:
                        raise ValueError(f"Field with id '{property_id}' is not a property.")

                equ = await PlayerUtils.chek_mogage_for_player(session_id=session_id, player_id=player_id, property_id=property_id)

                if equ:
                    raise ValueError(f"Player with id '{player_id}' has a mogage.")

                game_field.owner_id = None
                await session.commit()

            await session.refresh(game_field)

            return game_field.owner_id

    @staticmethod
    async def update_improvement(session_id: int, property_id: int, increase: bool):
        async with session_factory() as session:
            async with session.begin():
                result = await session.execute(
                    select(Board)
                    .filter((Board.game_session_id == session_id))
                    .filter(Board.property_id == property_id)
                )

                game_field = result.scalars().first()

                if game_field.owner_id is None:
                    raise ValueError(f"Field with id '{property_id}' does not have an owner.")

                mono = await session.execute(
                    select(Propertie)
                    .filter(Propertie.id == property_id)
                )

                field_data = mono.scalars().one_or_none()

                if field_data is None:
                    raise ValueError(f"Field with id '{property_id}' does not exist.")

                chek = await PlayerUtils.check_monopoly_for_player(
                    session_id=session_id,
                    player_id=game_field.owner_id,
                    color=field_data.street_color
                )

                if not chek:
                    raise ValueError(f"Player with id '{game_field.owner_id}' does not have a monopoly.")

                mogage = await PlayerUtils.chek_mogage_for_player(
                    session_id=session_id,
                    player_id=game_field.owner_id,
                    property_id=game_field.property_id
                )

                if mogage:
                    raise ValueError(f"Player with id '{game_field.owner_id}' has a mogage.")

                if game_field.type != 'prop':
                    if game_field.type != 'special':
                        pass
                    else:
                        raise ValueError(f"Field with id '{property_id}' is not a property.")

                hotels = game_field.hotel_level
                if hotels == 0 and increase == False:
                    raise ValueError(f"hotel_level of field with id '{property_id}' is already 0.")
                if hotels == 5 and increase == True:
                    raise ValueError(f"hotel_level {property_id} is max.")

                if increase:
                    game_field.hotel_level += 1
                else:
                    game_field.hotel_level -= 1

                print(game_field.hotel_level)

            await session.commit()
            await session.refresh(game_field)

            return game_field.hotel_level

    @staticmethod
    async def update_mortgage(session_id: int, property_id: int, mortgage: bool):
        async with session_factory() as session:
            async with session.begin():
                result = await session.execute(
                    select(Board)
                    .filter((Board.game_session_id == session_id))
                    .filter(Board.property_id == property_id)
                )

                game_field = result.scalars().first()

                if game_field.owner_id is None:
                    raise ValueError(f"Field with id '{property_id}' does not have an owner.")

                if game_field.type != 'prop':
                    if game_field.type != 'special':
                        pass
                    else:
                        raise ValueError(f"Field with id '{property_id}' is not a property.")

                hotels = game_field.hotel_level

                if hotels != 0 and mortgage == True:
                    raise ValueError(f"Need destroy hotels.")

                if mortgage:
                    game_field.mortgage = 1
                else:
                    game_field.mortgage = 0

                await session.commit()

            await session.refresh(game_field)

            return game_field.mortgage

    @staticmethod
    async def update_position(session_id: str, player_id: str, new_position: int):
        return await PlayerUtils.update_player_attribute(session_id, player_id, 'position', new_position % 10)

    @staticmethod
    async def update_balance(session_id: str, player_id: str, new_balance: int):
        return await PlayerUtils.update_player_attribute(session_id, player_id, 'balance', new_balance)

    @staticmethod
    async def update_part_balance(session_id: str, player_id: int, delta_balance: int):
        async with session_factory() as session:
            async with session.begin():
                result = await session.execute(
                    select(Player).filter(
                        Player.game_session_id == session_id,
                        Player.id == player_id
                    )
                )
                player = result.scalars().one_or_none()

                if player:
                    player.balance += delta_balance
                else:
                    raise HTTPException(status_code=404, detail="Player not found")
            await session.commit()
            await session.refresh(player)
            return player

    @staticmethod
    async def change_owner_posession(session_id: int, player_id: int, property_id: int):
        async with session_factory() as session:
            async with session.begin():
                try:
                    result = await session.execute(
                        select(Board)
                        .filter((Board.game_session_id == session_id))
                        .filter(Board.property_id == property_id)
                    )
                except Exception as e:
                    raise ValueError(f"Field with id '{property_id}' does not exist.")

                game_field = result.scalars().first()

                if game_field.type != 'prop':
                    if game_field.type != 'special':
                        pass
                    else:
                        raise ValueError(f"Field with id '{property_id}' is not a property.")

                game_field.owner_id = player_id
                await session.commit()
            await session.refresh(game_field)
            return game_field.owner_id

