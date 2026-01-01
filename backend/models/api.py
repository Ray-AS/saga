from backend.models.game import Choice
from pydantic import BaseModel, field_validator


class ChoiceWithID(Choice):
    id: int


class StoryAdvancementResponse(BaseModel):
    full: str
    condensed: str
    choices: list[ChoiceWithID]

    @field_validator('choices')
    @classmethod
    def validate_choices_have_ids(cls, v: list[BaseModel]):
        for c in v:
            if 'id' not in c.model_fields_set:
                raise KeyError('choice(s) does not contain id')
        return v


class StoryStartResponse(StoryAdvancementResponse):
    playthrough_id: str
