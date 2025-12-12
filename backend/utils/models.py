from typing import TypedDict


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


class Response(TypedDict):
    full: str
    condensed: str
    key: str
    characters: list[dict[str, str]]
    choices: list[str]
