from backend.utils.character import Character
from backend.utils.logger import logger
from backend.utils.models import Turn


class Playthrough:
    def __init__(self):
        self.story: list[str] = []
        self.history: list[Turn] = []

        # Irrelevant for now
        self.mc: Character | None = None

    def generate_character(self, name: str):
        self.mc = Character(name)
        logger.log_character_generated(self.mc.name)

    def generate_story_summary(self):
        return '\n\n'.join(self.story)

    def generate_turn_summary(self):
        lines: list[str] = []

        for i, turn in enumerate(self.history, start=1):
            lines.append(f'[TURN {i}]')
            lines.append('YOU:')
            lines.append(turn['user'] or '[no action]')
            lines.append('')
            lines.append('AI:')
            lines.append(turn['ai'])
            lines.append('')

        return '\n'.join(lines).strip()
