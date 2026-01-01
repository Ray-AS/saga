from backend.game.character import Character
from backend.models.game import Act, Choice, NarrativeState, StatBlock, Turn


class PlaythroughState:
    def __init__(self):
        self.story: list[str] = []
        self.history: list[Turn] = []
        self.character = Character()
        self.narrative = NarrativeState()
        self.current_choices: list[Choice] = []

    def record_turn(self, story: str, turn: Turn):
        self.story.append(story)
        self.history.append(turn)

    # convert current state into dictionary
    def to_dict(self):
        return {
            'story': self.story,
            'history': [turn.model_dump() for turn in self.history],
            'choices': [choice.model_dump() for choice in self.current_choices],
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

    # create instance of playthrough based on provided data
    @classmethod
    def from_dict(cls, data: dict):
        state = cls()
        state.story = data.get('story', [])
        state.history = [Turn(**t) for t in data.get('history', [])]
        state.current_choices = [Choice(**c) for c in data.get('choices', [])]

        character_data = data.get('character', {})
        state.character.name = character_data.get('name', '')
        state.character.stats = StatBlock(**character_data.get('stats', {}))
        state.character.stat_progress = character_data.get('stat_progress', {})

        narrative_data = data.get('narrative', {})
        state.narrative.act = Act[narrative_data.get('act', '')]
        state.narrative.progress = narrative_data.get('progress', 0.0)

        return state
