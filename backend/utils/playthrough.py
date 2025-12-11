from character import Character
from logger import logger
from world import World


class Playthrough:
    def __init__(self, difficulty: str, genre: str, length: int, mc: Character):
        self.difficulty = difficulty  # Not going to implement for now
        self.genre = genre
        self.length = length
        self.mc = mc
        self.world: World | None = None
        self.story: list[str] = []
        self.interactions: int = 0

    def generate_world(
        self, name: str, location: str, description: str, characters_involved: list[str]
    ):
        self.world = World(name, location)
        logger.log_world_generated(name)
        self.world.add_event(description, characters_involved)

    def generate_summary(self):
        return '\n'.join(self.story)
