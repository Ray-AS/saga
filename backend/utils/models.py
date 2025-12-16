from textwrap import dedent
from typing import TypedDict

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

# OUTPUT FORMAT
{format}
"""


class Response(BaseModel):
    full: str
    condensed: str
    choices: list[str]


FORMAT: str = dedent("""
Construct your response as a single, valid JSON object following this schema:
{
    full (str): "entire description of events (250-300 words)",
    condensed (str): "short description of events; keep only essentials that affect future story logic (100 words / 3-4 sentences)",
    choices (list[str]): "available options for the player to proceed; must be unique and make sense for the narrative (e.g. ["option 1", "option 2"])"
}
""").strip()
