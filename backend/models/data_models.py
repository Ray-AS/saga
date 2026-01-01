from backend.database.db import Base
from sqlalchemy import JSON, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


# all encompassing table schema: relates to story, history, choices, and character
class GameSession(Base):
    __tablename__ = 'game_sessions'

    id = Column(Integer, primary_key=True)
    act = Column(String)
    progress = Column(Float)
    character_id = Column(
        Integer, ForeignKey('characters.id', ondelete='CASCADE'), nullable=False
    )

    # relate session to story, history, etc. tables and ensure when session is deleted, all related elements are also deleted
    story_entries = relationship(
        'StoryEntry',
        back_populates='session',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )
    choices = relationship(
        'Choice',
        back_populates='session',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )
    history_entries = relationship(
        'HistoryEntry',
        back_populates='session',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )
    # one-to-one relationship for character (i.e. character can only belong to one playthrough)
    character = relationship(
        'Character',
        back_populates='session',
        cascade='all, delete-orphan',
        single_parent=True,
    )


class StoryEntry(Base):
    __tablename__ = 'story_entries'

    id = Column(Integer, primary_key=True)
    session_id = Column(
        Integer, ForeignKey('game_sessions.id', ondelete='CASCADE'), nullable=False
    )
    text = Column(String, nullable=False)
    # ensure story order is preserved when reading back from database
    order = Column(Integer, nullable=False)

    session = relationship('GameSession', back_populates='story_entries')


class Choice(Base):
    __tablename__ = 'choices'

    id = Column(Integer, primary_key=True)
    session_id = Column(
        Integer, ForeignKey('game_sessions.id', ondelete='CASCADE'), nullable=False
    )
    description = Column(String, nullable=False)
    difficulty = Column(String)
    type = Column(String)

    session = relationship('GameSession', back_populates='choices')


class HistoryEntry(Base):
    __tablename__ = 'history_entries'
    id = Column(Integer, primary_key=True)
    session_id = Column(
        Integer, ForeignKey('game_sessions.id', ondelete='CASCADE'), nullable=False
    )
    user = Column(String)
    ai = Column(String)
    # ensure story order is preserved when reading back from database
    order = Column(Integer)

    session = relationship('GameSession', back_populates='history_entries')


class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    stats = Column(JSON)
    stat_progress = Column(JSON)

    session = relationship('GameSession', back_populates='character', uselist=False)
