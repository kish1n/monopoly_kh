from typing import List

from fastapi import HTTPException
from sqlalchemy.future import select

from src.database import session_factory
from src.models import Player, GameSession, Board, Propertie
from src.data.schemas import PropertyModel, GamerModel
from src.data.utils import DataGetter, DataUpdater, DataSorted, DataChecker


class GameUtils:
    @staticmethod
    async def join_game_session(session_id: str, player_name: str):
        async with session_factory() as session:
            async with session.begin():
                game_session = await DataGetter.get_game_session(session, session_id)

                result = await session.execute(
                    select(Player).filter_by(game_session_id=session_id)
                )
                existing_players = result.scalars().all()
                new_q_value = len(existing_players)

                if (new_q_value + 1) > 4:
                    raise ValueError("Game session is full")

                new_player = Player(
                    game_session_id=session_id,
                    name=player_name,
                    q=new_q_value
                )
                session.add(new_player)

            await session.commit()
            await session.refresh(new_player)
            return new_player.id

    @staticmethod
    async def get_possessions_state(session_id: int):
        async with session_factory() as session:
            game_session = await DataGetter.get_game_session(session, session_id)
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

            # Получаем всех игроков в сессии
            players = await DataGetter.get_all_players_in_session(session, session_id)

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

            # Получаем игровые поля
            playground = await session.execute(
                select(Board).filter(Board.game_session_id == session_id)
            )
            playground = playground.scalars().all()

            for prop in playground:
                qur_property = await DataGetter.get_property_by_id(session, prop.property_id)
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
    async def make_trade(
            session_id: int,
            sender_player_id: int, sender_amount: int, sender_properties: List[str],
            target_player_id: int, target_amount: int, target_properties: List[str]
    ):
        async with session_factory() as session:
            async with session.begin():
                # Получаем игроков-участников сделки
                sender = await DataGetter.get_player_by_id(session, sender_player_id, session_id)
                target = await DataGetter.get_player_by_id(session, target_player_id, session_id)

                if sender.balance < sender_amount or target.balance < target_amount:
                    raise ValueError("Player does not have enough money")

                sender.balance = sender.balance + target_amount - sender_amount
                target.balance = target.balance - target_amount + sender_amount

                play_ground = await session.execute(
                    select(Board).filter(Board.game_session_id == session_id)
                )
                play_ground = play_ground.scalars().all()

                play_ground = sorted(play_ground, key=lambda x: x.property_id)

                if sender_properties:
                    await DataChecker.check_properties_and_update_ownership(
                        session, sender_properties, play_ground, session_id, sender_player_id, target_player_id)

                if target_properties:
                    await DataChecker.check_properties_and_update_ownership(
                        session, target_properties, play_ground, session_id, target_player_id, sender_player_id)

            return {"status": "ok"}

#DataChecker надо переделать на ексекьут
    @staticmethod
    async def buy_possesion(session_id: int, player_id: int, property_id: int):
        async with session_factory() as session:
            async with session.begin():
                game_session = await DataGetter.get_game_session(session, session_id)

                player = await DataGetter.get_player_by_id(session, player_id, session_id)

                field = await DataGetter.get_game_field(session, property_id, session_id)

                propertie = await DataGetter.get_property_by_id(session, property_id)

                await DataChecker.check_field_owner(field, player_id)

                if propertie.price is None:
                    raise ValueError(f"Field with id '{property_id}' is not a property. {field.property_id}")

                if player.balance < propertie.price:
                    raise ValueError(f"Player with id '{player_id}' does not have enough money.")

                if field.type != 'prop':
                    if field.type != 'special':
                        pass
                    raise ValueError(f"Field with id '{property_id}' is not a property. {field}")

                if player.position != field.property_id:
                    raise ValueError(f"Player with id '{player_id}' is not on field with property_id '{property_id}'.")

                field.owner_id = player_id
                player.balance -= propertie.price

            await session.commit()
            await session.refresh(player)
            await session.refresh(field)
            return player.balance

    @staticmethod
    async def sell_possession(session_id: int, player_id: int, property_id: int):
        async with session_factory() as session:
            async with session.begin():
                game_field = await DataGetter.get_game_field(session, property_id, session_id)

                await DataChecker.check_field_owner(game_field, player_id)

                if game_field.type != 'prop':
                    if game_field.type != 'special':
                        pass
                    else:
                        raise ValueError(f"Field with id '{property_id}' is not a property.")

                equ = await DataChecker.chek_mogage_for_player(session, session_id=session_id,
                                                               player_id=player_id, property_id=property_id)
                if equ:
                    raise ValueError(f"Player with id '{player_id}' has a mortgage.")

                game_field.owner_id = None
                await session.commit()

            await session.refresh(game_field)

            return game_field.owner_id

    @staticmethod
    async def update_improvement(session_id: int, property_id: int, increase: bool):
        async with session_factory() as session:
            async with session.begin():
                game_field = await DataGetter.get_game_field(session, property_id, session_id)
                await DataChecker.check_field_owner(game_field, game_field.owner_id)

                field_data = await DataGetter.get_game_property(session, property_id)
                if not field_data:
                    raise ValueError(f"Field with id '{property_id}' does not exist.")

                has_monopoly = await DataChecker.check_monopoly_for_player(
                    session, session_id, game_field.owner_id, field_data.street_color
                )
                if not has_monopoly:
                    raise ValueError(f"Player with id '{game_field.owner_id}' does not have a monopoly.")

                has_mortgage = await DataChecker.chek_mogage_for_player(
                    session, session_id, game_field.owner_id, game_field.property_id
                )
                if has_mortgage:
                    raise ValueError(f"Player with id '{game_field.owner_id}' has a mortgage.")

                if game_field.type != 'prop':
                    if game_field.type != 'special':
                        pass
                    else:
                        raise ValueError(f"Field with id '{property_id}' is not a property.")

                hotels = game_field.hotel_level
                if hotels == 0 and not increase:
                    raise ValueError(f"hotel_level of field with id '{property_id}' is already 0.")
                if hotels == 5 and increase:
                    raise ValueError(f"hotel_level {property_id} is max.")

                game_field.hotel_level += 1 if increase else -1

            await session.commit()
            await session.refresh(game_field)

        return game_field.hotel_level

    @staticmethod
    async def update_mortgage(session_id: int, property_id: int, mortgage: bool):
        async with session_factory() as session:
            async with session.begin():
                game_field = await DataGetter.get_game_field(session, property_id, session_id)
                await DataChecker.check_field_owner(game_field, game_field.owner_id)

                # Проверяем тип поля
                if game_field.type != 'prop' and game_field.type != 'special':
                    raise ValueError(f"Field with id '{property_id}' is not a property.")

                # Проверяем наличие улучшений
                hotels = game_field.hotel_level
                if hotels != 0 and mortgage:
                    raise ValueError("Need to destroy hotels before mortgaging the property.")

                # Обновляем статус ипотеки
                game_field.mortgage = 1 if mortgage else 0

                await session.commit()

            await session.refresh(game_field)
            return game_field.mortgage

    @staticmethod
    async def update_part_balance(session_id: str, player_id: int, delta_balance: int):
        async with session_factory() as session:
            async with session.begin():
                player = await DataGetter.get_player_by_id(session, player_id, session_id)
                player.balance += delta_balance

                await session.commit()
                await session.refresh(player)
            return player

    @staticmethod
    async def change_owner_posession(session_id: int, player_id: int, property_id: int):
        async with session_factory() as session:
            async with session.begin():
                game_field = await DataGetter.get_game_field(session, property_id, session_id)

                if game_field.type not in ['prop', 'special']:
                    raise ValueError(f"Field with id '{property_id}' is not a property.")

                game_field.owner_id = player_id
                await session.commit()
                await session.refresh(game_field)
            return game_field.owner_id

    @staticmethod
    async def update_position(session_id: str, player_id: str, new_position: int):
        return await DataUpdater.update_player_attribute(session_id, player_id, 'position', new_position % 10)

    @staticmethod
    async def update_balance(session_id: str, player_id: str, new_balance: int):
        return await DataUpdater.update_player_attribute(session_id, player_id, 'balance', new_balance)
