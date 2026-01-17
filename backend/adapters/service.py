from sqlalchemy.orm import Session

from backend.database.db_uploader import DBUploader
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

INTENT_MOD = {
    Intent.CAREFUL: 2,
    Intent.STANDARD: 0,
    Intent.BOLD: -2,
    Intent.DESPERATE: -4,
}


class GameService:
    def __init__(self, db: Session):
        self.engine = GameEngine()
        self.storyteller = Storyteller()
        self.uploader = DBUploader(db)
        self.states: dict[str, PlaythroughState] = {}

    # load all sessions from database
    def load_all_sessions(self):
        ids = self.uploader.list_ids()
        for id in ids:
            data = self.uploader.load(id)
            self.states[id] = PlaythroughState.from_dict(data)

    # get state from database if exists
    def get_session(self, id: str) -> PlaythroughState:
        if id not in self.states:
            data = self.uploader.load(id)
            self.states[id] = PlaythroughState.from_dict(data)
        return self.states[id]

    def start_game(self):
        story, choice_block = self.storyteller.generate_start()
        choices = choice_block.choices

        initial_turn = Turn(user='[Character created]', ai=story.condensed)

        state = PlaythroughState()
        state.record_turn(story.full, initial_turn)
        state.current_choices = choices

        # upload to database
        data = state.to_dict()
        session_id = self.uploader.save(data)
        self.states[session_id] = state

        return StoryStartResponse(
            playthrough_id=session_id,
            full=story.full,
            condensed=story.condensed,
            choices=choices,
        )

    def advance_game(self, session_id: str, choice: ChoiceInfo):
        state = self.get_session(session_id)

        # calculate success
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
        state.current_choices = choice_block.choices if not story.is_ending else []
        advance_narrative(state.narrative, success)

        # save to database
        data = state.to_dict()
        self.uploader.save(data, session_id)

        print(
            state.narrative.act, state.narrative.progress, state.narrative.allow_ending
        )

        return StoryAdvanceResponse(
            playthrough_id=session_id,
            full=story.full,
            condensed=story.condensed,
            choices=choice_block.choices if not story.is_ending else [],
            success=success,
        )

    def summarize_game(self, session_id: str):
        pass
