from typing import NamedTuple

from groq.types.chat import ChatCompletionMessageParam as Message
from pydantic import BaseModel


class Turn(BaseModel):
    user: str
    ai: str


class Response(BaseModel):
    full: str
    condensed: str
    choices: list[str]


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

# OUTPUT FORMAT
{format}
"""
