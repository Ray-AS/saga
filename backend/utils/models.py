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


MessageTemplate: str = """
# ROLE
{role}

# STYLE CONSTRAINTS
{style_constraints}

# ACTION CONSTRAINTS
{action_constraints}

# OUTPUT FORMAT
{format}

# CONTEXT HISTORY (Past Turns)
{history}

# PLAYER ACTION
{player_action}
"""
