from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.database import Base
from uuid import uuid4

class GameSession(Base):
    __tablename__ = 'game_session'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String, unique=True, index=True, default=str(uuid4))
    status = Column(String, default="waiting")
    current_player_index = Column(Integer, default=0)
    max_players = Column(Integer, default=4)
    current_players_count = Column(Integer, default=0)

    players = relationship("GameUser", back_populates="session")

class GameUser(Base):
    __tablename__ = 'game_user'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, index=True, unique=True, default=None, nullable=True)
    name = Column(String)
    money = Column(Integer, default=1500)
    position = Column(Integer, default=0)
    queue = Column(Integer, default=0)
    in_jail = Column(Boolean, default=False)
    session_id = Column(Integer, ForeignKey('game_session.id'))

    session = relationship("GameSession", back_populates="players")