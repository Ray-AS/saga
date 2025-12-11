from typing import TypedDict


class Event(TypedDict):
    description: str
    location: str
    characters_involved: list[str] | None


class NPC(TypedDict):
    name: str
    background: str
