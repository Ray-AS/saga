from backend.utils.logger import logger
from backend.utils.models import Turn
from backend.utils.playthrough import Playthrough
from backend.utils.storyteller import Storyteller


class Game:
    def __init__(self):
        self.storyteller = Storyteller()
        self.playthrough = Playthrough()

    def initialize(self):
        # Generate main character (irrelevant to gameplay for now)
        name = input('Enter character name: ')
        self.playthrough.generate_character(name)

        # Generate a random start to a story
        starting_event = self.storyteller.generate_start()
        turn: Turn = {'user': 'created character', 'ai': starting_event.condensed}

        # Update story state with starting data
        self.update_playthrough(starting_event.full, turn)

        return starting_event.choices

    def play(self):
        game_over = False
        # Initialize story and get starting choices
        choices: list[str] = self.initialize()
        history = self.playthrough.history
        turn: Turn = {'user': '', 'ai': ''}

        while not game_over:
            # If there are no choices, just generate story with no player action
            if not choices:
                outcome = self.storyteller.generate_outcome(history)
            else:
                num_choices = len(choices)
                # Display all choices to user
                print('---CHOICES---')
                for i in range(0, num_choices):
                    print(f'{i + 1}: {choices[i]}')

                choice = int(input(f'Choose (1 - {num_choices}): ')) - 1

                if choice not in range(0, num_choices):
                    break

                # Generate outcome based on decision
                turn['user'] = choices[choice]
                outcome = self.storyteller.generate_outcome(history, choices[choice])

            # Update story state
            turn['ai'] = outcome[1].condensed
            story = outcome[1].full

            if story == 'failed' or turn['ai'] == 'failed':
                break

            self.update_playthrough(story, turn)

            # Update choices
            choices = outcome[1].choices

        print('\n---STORY SUMMARY---')
        print(self.playthrough.generate_summary())

    def update_playthrough(self, story: str, turn: Turn):
        # Update playthrough state and log story progression
        self.playthrough.story.append(story)
        self.playthrough.history.append(turn)
        logger.log_story(story, turn)
