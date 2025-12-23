from typing import NamedTuple

from backend.utils.models.game_models import Choice
from groq.types.chat import ChatCompletionMessageParam as Message
from pydantic import BaseModel


class Response(BaseModel):
    full: str
    condensed: str
    choices: list[Choice]


class StoryOutcome(NamedTuple):
    messages: list[Message]
    response: Response


SystemMessageContent: str = """
# ROLE
{role}

# STYLE CONSTRAINTS
{style_constraints}

# ACTION CONSTRAINTS
{action_constraints}

# STORY PROGRESSION DESCRIPTION
{progression_description}

# CHOICE SCHEMA
{choice_schema}

# OUTPUT FORMAT
{format}
"""
