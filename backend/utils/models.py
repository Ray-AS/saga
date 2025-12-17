from textwrap import dedent
from typing import NamedTuple, TypedDict

from groq.types.chat import ChatCompletionMessageParam as Message
from pydantic import BaseModel


class Turn(TypedDict):
    user: str
    ai: str


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


class Response(BaseModel):
    full: str
    condensed: str
    choices: list[str]


class StoryOutcome(NamedTuple):
    messages: list[Message]
    response: Response


PROGRESSION_DESCRIPTION = """A single response represents exactly one turn:
- Resolve the player's last choice
- Update the world state
- Present new choices
- Do not resolve any future choices"""


FORMAT: str = dedent("""
Construct your response as a single, valid JSON object following this schema:
{
    full (str): "entire description of events (150-300 words; longer for important scenes, shorter for unimportant)",
    condensed (str): "short description of events; keep only essentials that affect future story logic (50-100 words / 3-4 sentences)",
    choices (list[str]): "available options for the player to proceed; must be unique and make sense for the narrative (e.g. ["option 1", "option 2"])"
}
""").strip()
