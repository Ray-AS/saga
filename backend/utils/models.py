from textwrap import dedent
from typing import TypedDict

from pydantic import BaseModel


class Event(TypedDict):
    description: str
    location: str
    characters_involved: list[str] | None


class NPC(TypedDict):
    name: str
    background: str


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
    key: str
    characters: list[dict[str, str]]
    choices: list[str]


class CondensedResponse(BaseModel):
    full: str
    condensed: str
    choices: list[str]


COMPLETE_FORMAT: str = dedent("""
Construct your response as a single, valid JSON object following this schema:
{
    full (str): "entire description of events (150-250 words)",
    condensed (str): "short description of events; keep only essentials that affect future story logic (30-50 words)",
    key (str): "one sentence description of events (8-15 words)",
    characters (list[dict{"name": "Frodo", "action": "Threw ring into the fire."}]): "characters involved in the events and what they did"
    choices (list[str]): "available options for the player to proceed; must be unique and make sense for the narrative (e.g. ["option 1", "option 2"])"
}
""").strip()

CONDENSED_FORMAT: str = dedent("""
Construct your response as a single, valid JSON object following this schema:
{
    full (str): "entire description of events (250-300 words)",
    condensed (str): "short description of events; keep only essentials that affect future story logic (100 words / 3-4 sentences)",
    choices (list[str]): "available options for the player to proceed; must be unique and make sense for the narrative (e.g. ["option 1", "option 2"])"
}
""").strip()
