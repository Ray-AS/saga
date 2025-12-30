from backend.game.character import Character
from backend.models.game import NarrativeState, Turn


class PlaythroughState:
    def __init__(self):
        self.story: list[str] = []
        self.history: list[Turn] = []
        self.character = Character()
        self.narrative = NarrativeState()

    def record_turn(self, story: str, turn: Turn):
        self.story.append(story)
        self.history.append(turn)
