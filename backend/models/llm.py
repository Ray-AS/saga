from typing import NamedTuple

from backend.models.game import Choice
from groq.types.chat import ChatCompletionMessageParam as Message
from pydantic import BaseModel, field_validator


class StoryResponse(BaseModel):
    full: str
    condensed: str

    @field_validator('full')
    @classmethod
    def validate_full_length(cls, v):
        if len(v.split()) not in range(50, 400):
            raise ValueError('Full story description word count invalid')
        return v

    @field_validator('condensed')
    @classmethod
    def validate_condensed_length(cls, v):
        if len(v.split()) not in range(10, 200):
            raise ValueError('Condensed story description word count invalid')
        return v


class ChoiceResponse(BaseModel):
    choices: list[Choice]

    @field_validator('choices')
    @classmethod
    def validate_num_choices(cls, v):
        if len(v) not in range(3, 6):
            raise ValueError('Number of choices not within range')
        return v


class StoryOutcome(NamedTuple):
    messages: list[Message]
    story: StoryResponse
    choices: ChoiceResponse
