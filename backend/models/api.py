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
