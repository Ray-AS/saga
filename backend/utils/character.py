from backend.utils.models.playthrough_models import StatBlock


class Character:
    def __init__(self, name: str):
        self.name = name
        self.stats = StatBlock()
