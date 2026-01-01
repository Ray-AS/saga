import logging

from backend.game.state import PlaythroughState
from backend.models.game import Act, Choice

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

    def log_narrative_state(self, act: Act, progress: float, allow_ending: bool):
        logging.info(
            'NARRATIVE STATE | act=%s | progress=%.2f | allow_ending=%s',
            act.name,
            progress,
            allow_ending,
        )

    def log_narrative_transition(
        self,
        from_act: Act,
        to_act: Act,
    ):
        logging.info(
            'NARRATIVE_TRANSITION | %s → %s',
            from_act.name,
            to_act.name,
        )

    def log_story_end(
        self,
        act: Act,
        progress: float,
    ):
        logging.info(
            'STORY_END | act=%s | progress=%.2f',
            act.name,
            progress,
        )


logger = GameLogger()
