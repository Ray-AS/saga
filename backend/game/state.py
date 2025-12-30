from backend.game.character import Character
from backend.models.game import Turn


class PlaythroughState:
    def __init__(self):
        self.story: list[str] = []
        self.history: list[Turn] = []
        self.character = Character()

    def record_turn(self, story: str, turn: Turn):
        self.story.append(story)
        self.history.append(turn)
