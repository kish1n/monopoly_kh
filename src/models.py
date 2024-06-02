from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from src.database import Base

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

