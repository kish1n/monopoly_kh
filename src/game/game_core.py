from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.future import select
from src.game.entities.Dice import Dice

from src.database import session_factory
from src.game.database import Player, GameSession


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
    async def update_improvement(session_id: int, index: int, increase: bool):
        async with session_factory() as session:
            async with session.begin():
                result = await session.execute(select(GameSession).filter_by(id=session_id))
                game_session = result.scalars().first()

                if not game_session:
                    raise ValueError(f"Game session with id '{session_id}' does not exist.")

                possessions_state = game_session.possessions_state
                index_str = str(index)

                if index_str not in possessions_state:
                    raise ValueError(f"Index '{index_str}' not found in possessions_state.")

                if possessions_state[index_str]['mortgage']:
                    raise ValueError(f"Cannot update improvement for mortgaged property.")

                improvement = possessions_state[index_str]['improvement']

                if increase:
                    if improvement < 5:
                        possessions_state[index_str]['improvement'] += 1
                else:
                    if improvement > 0:
                        possessions_state[index_str]['improvement'] -= 1

                # Явно указываем на изменение поля
                game_session.possessions_state = possessions_state

                # Обновляем объект в сессии
                await session.execute(
                    update(GameSession).
                    where(GameSession.id == session_id).
                    values(possessions_state=possessions_state)
                )

            await session.commit()
            await session.refresh(game_session)

        return game_session.possessions_state

    @staticmethod
    async def update_mortgage(session_id: int, index: int, mortgage: bool):
        async with session_factory() as session:
            async with session.begin():
                result = await session.execute(select(GameSession).filter_by(id=session_id))
                game_session = result.scalars().first()
                if not game_session:
                    raise ValueError(f"Game session with id '{session_id}' does not exist.")

                possessions_state = game_session.possessions_state
                if index not in possessions_state:
                    raise ValueError(f"Index '{index}' not found in possessions_state.")

                improvement = possessions_state[index]['improvement']

                if mortgage:
                    possessions_state[index]['mortgage'] = True
                else:
                    if improvement == 0:
                        possessions_state[index]['mortgage'] = False
                    else:
                        raise ValueError("Cannot set mortgage to False when improvement is not 0.")

                game_session.possessions_state = possessions_state
                session.add(game_session)

            await session.commit()
            return game_session.possessions_state

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

    @staticmethod
    async def update_position(session_id: str, player_id: str, new_position: int):
        return await GameCore.update_player_attribute(session_id, player_id, 'position', new_position % 10)

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















    # @staticmethod
    # async def update_players_money(session_id: str, player_id: str, difference: int):
    #     async with session_factory() as session:
    #         async with session.begin():
    #             result = await session.execute(
    #                 select(Player).filter(
    #                     Player.session_id == session_id,
    #                     Player.user_id == player_id
    #                 )
    #             )
    #             player = result.scalars().first()
    #             if player:
    #                 player.money += difference
    #                 await session.commit()
    #                 await session.refresh(player)
    #                 return player
    #             else:
    #                 raise HTTPException(status_code=404, detail="Player not found")
    #
    # @staticmethod
    # async def update_player_queue(session_id: str, player_id: str, new_queue: int):
    #     # Call the universal update function
    #     return await GameCore.update_player_attribute(session_id, player_id, 'queue', new_queue)
    #
    # @staticmethod
    # async def update_player_position(session_id: str, player_id: str, new_position: int):
    #     # Call the universal update function
    #     return await GameCore.update_player_attribute(session_id, player_id, 'position', new_position % 40)
    #
    # @staticmethod
    # async def roll_dice_and_update_position(session_id: str, player_id: str):
    #     dice = Dice()
    #     roll_result = dice.roll()
    #
    #     async with session_factory() as session:
    #         async with session.begin():
    #             result = await session.execute(
    #                 select(Player).filter(Player.session_id == session_id, Player.user_id == player_id)
    #             )
    #             player = result.scalars().first()
    #             if not player:
    #                 raise HTTPException(status_code=404, detail="Player not found")
    #
    #             new_position = player.position + sum(roll_result)
    #             player.position = new_position % 40
    #             await session.commit()
    #             await session.refresh(player)
    #
    #     return roll_result, player
    #
    # @staticmethod
    # async def update_player_in_jail(session_id: str, player_id: str, in_jail: bool):
    #     # Call the universal update function
    #     return await GameCore.update_player_attribute(session_id, player_id, 'in_jail', in_jail)
    #
    #
    #
    #
