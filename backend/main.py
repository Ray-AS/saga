from backend.adapters.cli import CLIAdapter
from backend.game.engine import GameEngine
from backend.game.state import PlaythroughState
from backend.llm.storyteller import MODEL, Storyteller
from backend.utils.logger import logger
from backend.utils.uploader import FileUploader


def main():
    state = PlaythroughState()
    engine = GameEngine()
    storyteller = Storyteller()
    ui = CLIAdapter()
    uploader = FileUploader()

    logger.info('GAME_START')

    story, choice_block = storyteller.generate_start()
    logger.log_story(story.full)

    choices = choice_block.choices
    logger.log_choices(choices)

    while True:
        choice = ui.choose(choices)

        if choice == 'END':
            break

        intent_mod, intent = ui.choose_intent()

        success, turn = engine.resolve_turn(
            state, choice, intent_mod, choice.difficulty
        )

        logger.log_turn_resolution(
            choice=choice.choice_description,
            success=success.value,
            intent=intent,
        )

        story, choice_block = storyteller.generate_turn(
            state.history, choice.choice_description, success, intent
        )
        choices = choice_block.choices

        turn.ai = story.condensed
        state.record_turn(story.full, turn)

        logger.log_story(story.full)
        logger.log_state(state)
        logger.log_choices(choice_block.choices)

    uploader.output_to_file(state.story, state.history, MODEL)


if __name__ == '__main__':
    main()
