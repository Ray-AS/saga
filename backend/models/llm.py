from typing import NamedTuple

from backend.models.game import Choice
from groq.types.chat import ChatCompletionMessageParam as Message
from pydantic import BaseModel


class StoryResponse(BaseModel):
    full: str
    condensed: str


class ChoiceResponse(BaseModel):
    choices: list[Choice]


class StoryOutcome(NamedTuple):
    messages: list[Message]
    story: StoryResponse
    choices: ChoiceResponse
