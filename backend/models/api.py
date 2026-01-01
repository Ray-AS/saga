from backend.models.game import Choice, Intent, Success
from pydantic import BaseModel


class StoryStartResponse(BaseModel):
    playthrough_id: str
    full: str
    condensed: str
    choices: list[Choice]


class StoryAdvanceResponse(StoryStartResponse):
    success: Success


class ChoiceInfo(Choice):
    intent: Intent


class PlaythroughSummary(BaseModel):
    playthrough_id: str
    act: str
    progress: float
    can_end: bool
    summary: str


class ListPlaythroughsResponse(BaseModel):
    playthroughs: list[PlaythroughSummary] = []
