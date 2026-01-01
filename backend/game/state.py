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

    def to_dict(self):
        return {
            'story': self.story,
            'history': [turn.model_dump() for turn in self.history],
            'character': {
                'name': self.character.name,
                'stats': self.character.stats.model_dump(),
                'stat_progress': self.character.stat_progress,
            },
            'narrative': {
                'act': self.narrative.act.name,
                'progress': self.narrative.progress,
            },
        }

    @classmethod
    def from_dict(cls, data: dict):
        state = cls()
        state.story = data.get('story', [])
        state.history = [Turn(**t) for t in data.get('history', [])]

        character_data = data.get('character', {})
        state.character.name = character_data.get('name', '')
        state.character.stats = character_data.get('stats', {})
        state.character.stat_progress = character_data.get('stat_progress', {})

        narrative_data = data.get('narrative', {})
        state.narrative.act = narrative_data.get('act', '')
        state.narrative.progress = narrative_data.get('act', 0.0)

        return state
