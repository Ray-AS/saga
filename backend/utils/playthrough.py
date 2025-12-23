from backend.utils.character import Character
from backend.utils.logger import logger
from backend.utils.models.game_models import Turn


class Playthrough:
    """
    Represents a playthrough in an interactive story game (i.e. an individual story)

    Attributes:
        story (list[str]): list of paragraphs describing each point in story
        history (list[Turn]): list of Turn dicts describing player and ai action at each point in story
        mc (Character): object that represents the main character (player) of story
    """

    def __init__(self):
        self.story: list[str] = []
        self.history: list[Turn] = []

        # Irrelevant for now
        self.mc: Character = Character()

    def generate_character(self, name: str):
        """
        Generates an instance of Character class based on player input name to represent the main character

        Args:
            name (str): name of character
        """
        self.mc.name = name
        logger.log_character_generated(self.mc.name)

    def generate_story_summary(self):
        """
        Joins all paragraphs in story

        Returns:
            str: entire story in one string
        """
        return '\n\n'.join(self.story)

    def generate_turn_summary(self):
        """
        Joins all Turn dicts into one formatted string

        Returns:
            str: all turns in story
        """
        lines: list[str] = []

        for i, turn in enumerate(self.history, start=1):
            lines.append(f'[TURN {i}]')
            lines.append('YOU:')
            lines.append(turn.user or '[no action]')
            lines.append('')
            lines.append('AI:')
            lines.append(turn.ai)
            lines.append('')

        return '\n'.join(lines).strip()
