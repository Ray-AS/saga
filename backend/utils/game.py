from datetime import datetime
from pathlib import Path

from backend.utils.logger import logger
from backend.utils.models import Turn
from backend.utils.playthrough import Playthrough
from backend.utils.storyteller import Storyteller


class Game:
    """
    Represents an interactive story game

    Attributes:
        storyteller (Storyteller): object that dynamically generates story from user action
        playthrough (Playthrough): object that stores history of story and turns
    """

    def __init__(self):
        self.storyteller = Storyteller()
        self.playthrough = Playthrough()

    def update_playthrough(self, story: str, turn: Turn):
        """
        Updates the story and history attributes in playthrough class

        Args:
            story (str): paragraph(s) describing how the story advances
            turn (Turn): dict containing player decision and condensed story advancement
        """
        # Update playthrough state and log story progression
        self.playthrough.story.append(story)
        self.playthrough.history.append(turn)
        logger.log_story(story, turn)

    def upload_summary(self, story_summary: str, turn_summary: str):
        """
        Uploads summary of playthrough (i.e. story and turn history) to .txt file

        Args:
            story_summary (str): joined description of all story paragraphs
            turn_summary (str): joined and formatted play-by-play of each turn
        """
        filename = ''

        if self.playthrough.mc:
            filename += f'{self.playthrough.mc.name}_'

        current_datetime = datetime.now()
        timestamp_str = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
        filename += timestamp_str

        script_dir = Path(__file__).parent
        filepath = script_dir.parent / 'playthroughs' / f'{filename}.txt'

        with open(filepath, 'w') as f:
            f.write('---STORY SUMMARY---\n')
            f.write(story_summary)
            f.write('\n\n')
            f.write('---TURN SUMMARY---\n')
            f.write(turn_summary)

    def initialize(self):
        """
        Establishes the opening sequence of the playthrough story

        Returns:
            list[str]: choices for the player to proceed
        """
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
        """Creates the interactive story game loop and continues until user enters and invalid choice"""
        game_over = False
        # Initialize story and get starting choices
        choices: list[str] = self.initialize()
        history = self.playthrough.history

        while not game_over:
            turn: Turn = {'user': '', 'ai': ''}
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

        story_summary = self.playthrough.generate_story_summary()
        turn_summary = self.playthrough.generate_turn_summary()

        self.upload_summary(story_summary, turn_summary)

        print('\n---STORY SUMMARY---')
        print(story_summary)
        print('\n---TURN SUMMARY---')
        print(turn_summary)
