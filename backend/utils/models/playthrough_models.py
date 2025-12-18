from enum import Enum

from pydantic import BaseModel


class Turn(BaseModel):
    user: str
    ai: str


class Difficulty(str, Enum):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
    EXTREME = 'extreme'


class Stat(str, Enum):
    FORCE = 'force'
    GUILE = 'guile'
    INFLUENCE = 'influence'
    INSIGHT = 'insight'


class Choice(BaseModel):
    choice: str
    difficulty: Difficulty
    type: Stat
