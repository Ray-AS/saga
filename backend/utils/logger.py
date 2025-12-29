import logging

from backend.game.state import PlaythroughState
from backend.models.game import Choice

logging.basicConfig(level=logging.INFO)


class GameLogger:
    def info(self, msg: str):
        logging.info(msg)

    def log_story(self, text: str):
        logging.info('STORY:\n%s', text)

    def log_choices(self, choices: list[Choice]):
        for c in choices:
            logging.info(
                'CHOICE: %s | %s | %s',
                c.choice_description,
                c.type,
                c.difficulty,
            )

    def log_state(self, state: PlaythroughState):
        logging.info('STATS: %s', state.character.stats)
        logging.info('PROGRESS: %s', state.character.stat_progress)

    def log_turn_resolution(self, choice: str, success: str, intent: str):
        logging.info(
            'TURN: %s | SUCCESS=%s | INTENT=%s',
            choice,
            success,
            intent,
        )


logger = GameLogger()
