from datetime import datetime
from pathlib import Path

from backend.utils.configs.game_configs import INITIAL_STAT_COUNT
from backend.utils.logger import logger
from backend.utils.models.playthrough_models import Choice, Progress, Turn
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

    def get_choice(self, choices: list[Choice]) -> Choice:
        """
        Get a list of choices and return the choice player decides on

        Args:
            choices (list[Choice]): list of choices

        Returns:
            Choice: decision player makes
        """
        num_choices = len(choices)

        print('---CHOICES---')
        for i in range(num_choices):
            print(f'{i + 1}: {choices[i].choice_description}')

        choice_index = int(input(f'Choose (1 - {num_choices}): ')) - 1

        return choices[choice_index]

    def get_starting_stats(self):
        """
        Generates a short character creation sequence and returns the stats corresponding to player choices

        Returns:
            list[str]: list of stats for relevant character
        """
        context: list[Turn] = []
        stats: list[str] = []
        progress = Progress(current=1, end=INITIAL_STAT_COUNT)

        for i in range(progress.end + 1):
            turn = Turn(user='', ai='')

            response = self.storyteller.get_stat_scenario(context, progress)

            print('---FULL---')
            print(response.full)
            print('\n---CONDENSED---')
            print(response.condensed)
            print()

            if progress.current <= progress.end:
                choice = self.get_choice(response.choices)

                turn.user = choice.choice_description
                turn.ai = response.condensed

                stats.append(choice.type)
                context.append(turn)
                progress.current += 1

        return stats

    def increment_stats(self, stats: list[str]):
        """
        Get a list of stats and increment corresponding stats of player character

        Args:
            stats (list[str]): list of stats
        """
        for stat in stats:
            if self.playthrough.mc:
                player_stats = self.playthrough.mc.stats
                current = getattr(player_stats, stat)
                setattr(player_stats, stat, current + 1)

    def start_story(self):
        """
        Establishes the opening sequence of the playthrough story

        Returns:
            list[str]: choices for the player to proceed
        """
        # Generate main character (irrelevant to gameplay for now)
        name = input('Enter character name: ')
        self.playthrough.generate_character(name)
        self.increment_stats(self.get_starting_stats())
        assert self.playthrough.mc is not None
        logger.log_stats(self.playthrough.mc.stats)

        # Generate a random start to a story
        starting_event = self.storyteller.generate_start()
        turn = Turn(user='created character', ai=starting_event.condensed)

        # Update story state with starting data
        self.update_playthrough(starting_event.full, turn)

        return starting_event.choices

    def play(self):
        """Creates the interactive story game loop and continues until user enters and invalid choice"""
        game_over = False
        # Initialize story and get starting choices
        choices: list[Choice] = self.start_story()
        history = self.playthrough.history

        # NEED TO IMPLEMENT SUCCESS GRADE CALCULATION
        while not game_over:
            print(choices)
            turn = Turn(user='', ai='')
            # If there are no choices, just generate story with no player action
            if not choices:
                outcome = self.storyteller.generate_outcome(history)
            else:
                choice = self.get_choice(choices)

                # Determine level of success of choice and add tags
                # Assemble 'user' portion of turn
                # Update tension, act score, stat progression, tags

                # Generate outcome based on decision
                turn.user = choice.choice_description
                outcome = self.storyteller.generate_outcome(
                    history, choice.choice_description
                )

            # Update story state
            turn.ai = outcome.response.condensed
            story = outcome.response.full

            if story == 'failed' or turn.ai == 'failed':
                break

            self.update_playthrough(story, turn)

            # Update choices
            choices = outcome.response.choices

        story_summary = self.playthrough.generate_story_summary()
        turn_summary = self.playthrough.generate_turn_summary()

        self.upload_summary(story_summary, turn_summary)

        print('\n---STORY SUMMARY---')
        print(story_summary)
        print('\n---TURN SUMMARY---')
        print(turn_summary)
