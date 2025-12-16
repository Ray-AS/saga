from backend.utils.character import Character
from backend.utils.logger import logger
from backend.utils.models import Turn
from backend.utils.world import World


class Playthrough:
    def __init__(self):
        # self.difficulty = difficulty  # Not going to implement for now
        # self.genre = genre
        # self.length = length
        # self.interactions: int = 0
        self.mc: Character | None = None
        self.world: World | None = None
        self.story: list[str] = []
        self.history: list[Turn] = []

    def generate_character(self, name: str, character_class: str = ''):
        self.mc = Character(name, character_class)
        logger.log_character_generated(self.mc.name, self.mc.character_class)

    def generate_world(
        self, name: str, location: str, description: str, characters_involved: list[str]
    ):
        self.world = World(name, location)
        logger.log_world_generated(self.world.name)
        self.world.add_event(description, characters_involved)

    def generate_summary(self):
        return '\n'.join(self.story)
