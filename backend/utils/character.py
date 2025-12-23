from backend.utils.models.game_models import StatBlock, Stat


class Character:
    def __init__(self, name: str = ''):
        self.name = name
        self.stats = StatBlock()
        self.stat_progress = {
            Stat.FORCE: 0,
            Stat.GUILE: 0,
            Stat.INFLUENCE: 0,
            Stat.INSIGHT: 0,
        }
