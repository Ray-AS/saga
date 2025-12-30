from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field


class Act(Enum):
    SETUP = 1
    ESCALATION = 2
    RESOLUTION = 3


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


StatValue = Annotated[int, Field(ge=0, le=5)]


class StatBlock(BaseModel):
    force: StatValue = 0
    guile: StatValue = 0
    influence: StatValue = 0
    insight: StatValue = 0


class Choice(BaseModel):
    choice_description: str
    difficulty: Difficulty
    type: Stat


class Turn(BaseModel):
    user: str
    ai: str


class NarrativeState(BaseModel):
    act: Act = Act.SETUP
    progress: float = 0.0
