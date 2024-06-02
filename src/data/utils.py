from typing import List

from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.future import select

from src.database import session_factory
from src.models import Player, GameSession, Board, Propertie

class DataGetter:
    @staticmethod
    async def get_game_session(session, session_id: int):
        result = await session.execute(select(GameSession).filter_by(id=session_id))
        game_session = result.scalars().first()
        if not game_session:
            raise ValueError(f"Game session with id '{session_id}' does not exist.")
        return game_session

    @staticmethod
    async def get_property_by_id(session, property_id: int):
        result = await session.execute(
            select(Propertie).filter(Propertie.id == property_id)
        )
        property = result.scalars().one_or_none()
        if not property:
            raise ValueError(f"Property with id '{property_id}' does not exist.")
        return property

    @staticmethod
    async def get_player_by_id(session, player_id: int, session_id: int = None):
        query = select(Player).filter_by(id=player_id)
        if session_id:
            query = query.filter(Player.game_session_id == session_id)
        result = await session.execute(query)
        player = result.scalars().first()
        if not player:
            raise ValueError(f"Player with id '{player_id}' does not exist.")
        return player

    @staticmethod
    async def get_game_field(session, property_id: int, session_id: int):
        result = await session.execute(
            select(Board)
            .filter(Board.game_session_id == session_id)
            .filter(Board.property_id == property_id)
        )
        game_field = result.scalars().first()
        if not game_field:
            raise ValueError(f"Field with property_id '{property_id}' does not exist in session '{session_id}'.")
        return game_field

    @staticmethod
    async def get_prop_for_player(session, session_id: str, player_id: str):
        board = await session.execute(
            select(Board)
            .filter(Board.game_session_id == session_id)
            .filter(Board.owner_id == player_id)
        ).scalars().all()
        return board

    @staticmethod
    async def get_hotels_at_str(session, str_color: str, session_id: int):
        result = await session.execute(
            select(Propertie).filter(Propertie.street_color == str_color)
        )
        props = result.scalars().all()

        hotels = 0

        for prop in props:
            result = await session.execute(
                select(Board)
                .filter(Board.game_session_id == session_id)
                .filter(Board.property_id == prop.id)
            )
            board = result.scalars().one_or_none()
            if board:
                hotels += board.hotel_level

        return hotels

    @staticmethod
    async def get_all_players_in_session(session, session_id: int):
        result = await session.execute(
            select(Player).filter(Player.game_session_id == session_id)
        )
        players = result.scalars().all()
        if not players:
            raise ValueError(f"No players found in session with id '{session_id}'.")
        return players

    @staticmethod
    async def get_str_color_by_id(session, property_id: int):
        result = await session.execute(
            select(Propertie).filter(Propertie.id == property_id)
        )
        prop = result.scalars().one_or_none()

        if not prop:
            raise ValueError(f"Property with id '{property_id}' does not exist.")
        return prop.street_color

    @staticmethod
    async def get_game_property(session, property_id: int):
        result = await session.execute(
            select(Propertie).filter(Propertie.id == property_id)
        )
        return result.scalars().one_or_none()

class DataUpdater:
    @staticmethod
    async def update_player_attribute_new(session, session_id: str, id: str, attribute: str, value):
        async with session.begin():
            result = await session.execute(
                select(Player).filter(
                    Player.game_session_id == session_id,
                    Player.id == id
                )
            )
            player = result.scalars().first()
            if player:
                setattr(player, attribute, value)
            else:
                raise HTTPException(status_code=404, detail="Player not found")
        await session.commit()
        await session.refresh(player)
        return player

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

class DataChecker:
    @staticmethod
    async def check_field_owner(game_field, owner_id: int):
        if game_field.owner_id is None or game_field.owner_id != owner_id:
            return False
        return True

    @staticmethod
    async def check_monopoly_for_player(session, session_id: str, player_id: str, color: str):
        async with session.begin():
            player = await session.execute(
                select(Player)
                .filter(Player.game_session_id == session_id)
                .filter(Player.id == player_id)
            ).scalars().one_or_none()

            if player is None:
                raise HTTPException(status_code=404, detail="Player not found")

            fields = await session.execute(
                select(Propertie)
                .filter(Propertie.street_color == color)
            ).scalars().all()

            if not fields:
                raise HTTPException(status_code=404, detail="Color not found")

            playground = await session.execute(
                select(Board)
                .filter(Board.game_session_id == session_id)
                .filter(Board.owner_id == player_id)
            ).scalars().all()

            for field in playground:
                if field.owner_id != player_id:
                    return False
            return True

    @staticmethod
    async def chek_mogage_for_player(session, session_id: str, player_id: str, property_id: str):
        player = await session.execute(
            select(Player)
            .filter(Player.game_session_id == session_id)
            .filter(Player.id == player_id)
        ).scalars().one_or_none()

        if player is None:
            raise HTTPException(status_code=404, detail="Player not found")

        field = await session.execute(
            select(Board)
            .filter(Board.game_session_id == session_id)
            .filter(Board.property_id == property_id)
        ).scalars().one_or_none()

        if field is None:
            raise HTTPException(status_code=404, detail="Field not found")

        if field.owner_id != player_id:
            raise HTTPException(status_code=400, detail="Player is not an owner of this field")

        return field.mortgage

    @staticmethod
    async def check_properties_and_update_ownership(session, properties: List[str], play_ground, session_id: int,
                                                    current_owner_id: int, new_owner_id: int):

        for prop in properties:
            color = await DataGetter.get_str_color_by_id(session, int(prop))
            print("start hotels")
            hotels = await DataGetter.get_hotels_at_str(session, str_color=color, session_id=session_id)

            if hotels:
                raise ValueError("There are hotels on the street")
            try:
                index = int(prop) - 1
                if play_ground[index].owner_id != current_owner_id:
                    raise ValueError(f"Player with id '{current_owner_id}' is not the owner of property '{prop}'.")
                play_ground[index].owner_id = new_owner_id
            except Exception as e:
                raise ValueError(f"Property not found {e}")

class DataSorted:
    @staticmethod
    async def sorted_board_new(session, session_id: int):
        board = await session.execute(
            select(Board)
            .filter(Board.game_session_id == session_id)
        ).scalars().all()

        board = sorted(board, key=lambda x: x.property_id)

        return [{'property_id': field.property_id} for field in board]

