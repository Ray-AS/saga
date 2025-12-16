from backend.utils.logger import logger
from backend.utils.models import Turn
from backend.utils.playthrough import Playthrough
from backend.utils.storyteller import Storyteller


class Game:
    def __init__(self):
        self.storyteller = Storyteller()
        self.playthrough = Playthrough()

    def initialize(self):
        name = input('Enter character name: ')
        self.playthrough.generate_character(name)
        starting_event = self.storyteller.generate_start()
        turn: Turn = {'user': 'created character', 'ai': starting_event.condensed}
        self.update_playthrough(starting_event.full, turn)
        logger.log_story(starting_event.full, turn)
        return starting_event.choices

    def play(self):
        game_over = False
        choices: list[str] = self.initialize()
        history = self.playthrough.history
        turn: Turn = {'user': '', 'ai': ''}
        while not game_over:
            if not choices:
                outcome = self.storyteller.generate_outcome(history)
            else:
                num_choices = len(choices)
                print('---CHOICES---')
                for i in range(0, num_choices):
                    print(f'{i + 1}: {choices[i]}')
                choice = int(input(f'Choose (1 - {num_choices}): ')) - 1
                turn['user'] = choices[choice]
                outcome = self.storyteller.generate_outcome(history, choices[choice])

            turn['ai'] = outcome[1].condensed
            story = outcome[1].full
            self.update_playthrough(story, turn)

            choices = outcome[1].choices

            logger.log_story(story, turn)

    def update_playthrough(self, story: str, turn: Turn):
        self.playthrough.story.append(story)
        self.playthrough.history.append(turn)
