from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field


class Difficulty(str, Enum):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
    EXTREME = 'extreme'


class Intent(str, Enum):
    CAREFUL = 'careful'
    STANDARD = 'standard'
    BOLD = 'bold'
    DESPERATE = 'desperate'


class Stat(str, Enum):
    FORCE = 'force'
    GUILE = 'guile'
    INFLUENCE = 'influence'
    INSIGHT = 'insight'


class Success(str, Enum):
    C_FAIL = 'CRITICAL FAILURE'
    FAIL = 'FAILURE'
    PARTIAL = 'PARTIAL SUCCESS'
    SUCCESS = 'SUCCESS'
    C_SUCCESS = 'CRITICAL SUCCESS'


DEFAULT_STAT_VALUE = 0
StatValue = Annotated[int, Field(ge=0, le=5)]


class StatBlock(BaseModel):
    force: StatValue = DEFAULT_STAT_VALUE
    guile: StatValue = DEFAULT_STAT_VALUE
    influence: StatValue = DEFAULT_STAT_VALUE
    insight: StatValue = DEFAULT_STAT_VALUE


class Choice(BaseModel):
    choice_description: str
    difficulty: Difficulty | None = None
    type: Stat


class Turn(BaseModel):
    user: str
    ai: str


class Progress(BaseModel):
    current: int
    end: int
