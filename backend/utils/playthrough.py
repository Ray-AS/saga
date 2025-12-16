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

    def generate_summary(self):
        return '\n\n\t'.join(self.story)
