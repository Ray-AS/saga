from logger import logger


class Playthrough:
    def __init__(self, difficulty, genre, length, mc, world):
        self.difficulty = difficulty  # Not going to implement for now
        self.genre = genre
        self.length = length
        self.mc = mc
        self.world = world
        self.story = []
        self.interactions = 0

    def generate_summary(self):
        return '\n'.join(self.story)
