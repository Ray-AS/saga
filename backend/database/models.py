from sqlalchemy import Column, Float, ForeignKey, Integer, String

from database import Base


class GameSession(Base):
    __tablename__ = 'game_sessions'

    id = Column(Integer, primary_key=True, index=True)
    act = Column(String)
    progress = Column(Float)
