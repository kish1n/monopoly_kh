from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from src.database import Base

possessions_state = {
    #start
    1: {'improvement': 0, 'mortgage': False},
    #schanse
    3: {'improvement': 0, 'mortgage': False},
    #donat
    5: {'improvement': 0, 'mortgage': False},
    6: {'improvement': 0, 'mortgage': False},
    #surp
    8: {'improvement': 0, 'mortgage': False},
    9: {'improvement': 0, 'mortgage': False},
    #durka
    11: {'improvement': 0, 'mortgage': False},
    12: {'improvement': 0, 'mortgage': False},
    13: {'improvement': 0, 'mortgage': False},
    14: {'improvement': 0, 'mortgage': False},
    15: {'improvement': 0, 'mortgage': False},
    16: {'improvement': 0, 'mortgage': False},
    #schanse
    18: {'improvement': 0, 'mortgage': False},
    19: {'improvement': 0, 'mortgage': False},
    #metalis
    21: {'improvement': 0, 'mortgage': False},
    #surp
    23: {'improvement': 0, 'mortgage': False},
    24: {'improvement': 0, 'mortgage': False},
    25: {'improvement': 0, 'mortgage': False},
    26: {'improvement': 0, 'mortgage': False},
    27: {'improvement': 0, 'mortgage': False},
    28: {'improvement': 0, 'mortgage': False},
    29: {'improvement': 0, 'mortgage': False},
    #go to durka
    31: {'improvement': 0, 'mortgage': False},
    32: {'improvement': 0, 'mortgage': False},
    #schanse
    34: {'improvement': 0, 'mortgage': False},
    35: {'improvement': 0, 'mortgage': False},
    #surp
    37: {'improvement': 0, 'mortgage': False},
    38: {'improvement': 0, 'mortgage': False},
    39: {'improvement': 0, 'mortgage': False},
}

class Propertie(Base):
    __tablename__ = 'propertie'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    name = Column(String, unique=True, nullable=False)
    price = Column(Integer, nullable=True)
    street_color = Column(String, nullable=True)
    improvement_value = Column(ARRAY(Integer), nullable=True)
    rent_value = Column(ARRAY(Integer), nullable=True)


class GameSession(Base):
    __tablename__ = 'game_session'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    players = relationship("Player", back_populates="game_session")


class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, nullable=True)  # ID пользователя из системы аутентификации
    game_session_id = Column(Integer, ForeignKey('game_session.id'), nullable=False)
    q = Column(Integer, nullable=False, default=0)
    position = Column(Integer, default=0)
    balance = Column(Integer, default=1500)
    game_session = relationship("GameSession", back_populates="players")

GameSession.players = relationship("Player", order_by=Player.id, back_populates="game_session")


class Board(Base):
    __tablename__ = 'board'

    id = Column(Integer, primary_key=True, index=True)
    game_session_id = Column(Integer, ForeignKey('game_session.id'), nullable=False)
    property_id = Column(Integer, ForeignKey('propertie.id'), nullable=True)
    type = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('player.id'), nullable=True)  # Владелец, если есть
    game_session = relationship("GameSession", back_populates="board_fields")
    hotel_level = Column(Integer, default=0)
    mortgage = Column(Integer, default=0)
    property = relationship("Propertie")
    owner = relationship("Player", back_populates="owned_fields")

GameSession.board_fields = relationship("Board", order_by=Board.property_id, back_populates="game_session")
Player.owned_fields = relationship("Board", back_populates="owner")

