from typing import TypedDict


class Event(TypedDict):
    description: str
    location: str
    time: str
    characters_involved: list[str]


class NPC(TypedDict):
    name: str
    background: str
