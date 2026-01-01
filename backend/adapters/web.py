from backend.game.engine import GameEngine
from backend.game.narrative_progression import advance_narrative
from backend.game.state import PlaythroughState
from backend.llm.storyteller import Storyteller
from backend.models.api import (
    ChoiceInfo,
    StoryAdvanceResponse,
    StoryStartResponse,
)
from backend.models.game import Choice, Intent, Turn
from backend.utils.uploader import FileUploader

INTENT_MOD = {
    Intent.CAREFUL: 2,
    Intent.STANDARD: 0,
    Intent.BOLD: -2,
    Intent.DESPERATE: -4,
}


class WebAdapter:
    def __init__(self):
        self.engine = GameEngine()
        self.storyteller = Storyteller()
        self.uploader = FileUploader()
        self.states: dict[str, PlaythroughState] = {}

    def start(self):
        story, choice_block = self.storyteller.generate_start()

        initial_turn = Turn(user='[Character created]', ai=story.condensed)

        state = PlaythroughState()
        state.record_turn(story.full, initial_turn)

        data = state.to_dict()
        id = self.uploader.save(data)

        self.states[id] = state

        choices = choice_block.choices

        return StoryStartResponse(
            playthrough_id=id,
            full=story.full,
            condensed=story.condensed,
            choices=choices,
        )

    def advance(self, id: str, choice: ChoiceInfo):
        if id not in self.states:
            data = self.uploader.load(id)
            self.states[id] = PlaythroughState.from_dict(data)

        state = self.states[id]

        intent_mod = INTENT_MOD[choice.intent]
        success, turn = self.engine.resolve_turn(
            state, Choice(**choice.model_dump()), intent_mod
        )

        story, choice_block = self.storyteller.generate_turn(
            state.history,
            choice.choice_description,
            success,
            choice.intent,
            state.narrative,
        )

        turn.ai = story.condensed
        state.record_turn(story.full, turn)
        advance_narrative(state.narrative, success)

        data = state.to_dict()
        self.uploader.save(data, id)

        return StoryAdvanceResponse(
            playthrough_id=id,
            full=story.full,
            condensed=story.condensed,
            choices=choice_block.choices,
            success=success,
        )
