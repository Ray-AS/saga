from backend.adapters.cli import CLIAdapter
from backend.game.engine import GameEngine
from backend.game.narrative_progression import advance_narrative
from backend.game.state import PlaythroughState
from backend.llm.storyteller import MODEL, Storyteller
from backend.models.api import ChoiceWithID, StoryAdvancementResponse
from backend.models.game import Act, Choice
from backend.utils.logger import logger
from backend.utils.uploader import FileUploader


class WebAdapter:
    def __init__(self):
        self.state = PlaythroughState()
        self.engine = GameEngine()
        self.storyteller = Storyteller()
        self.ui = CLIAdapter()
        self.uploader = FileUploader()

    def generate_choices_with_ids(self, choices: list[Choice]) -> list[ChoiceWithID]:
        choices_with_ids: list[ChoiceWithID] = []
        for i, c in enumerate(choices):
            choices_with_ids.append(
                ChoiceWithID(
                    id=i,
                    choice_description=c.choice_description,
                    difficulty=c.difficulty,
                    type=c.type,
                )
            )
        return choices_with_ids

    def start(self):
        story, choice_block = self.storyteller.generate_start()
        choices = choice_block.choices

        return StoryAdvancementResponse(
            full=story.full,
            condensed=story.condensed,
            choices=self.generate_choices_with_ids(choices),
        )
