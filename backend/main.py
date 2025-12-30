from backend.adapters.cli import CLIAdapter
from backend.game.engine import GameEngine
from backend.game.narrative_progression import advance_narrative
from backend.game.state import PlaythroughState
from backend.llm.storyteller import MODEL, Storyteller
from backend.models.game import Act
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
    print()

    choices = choice_block.choices
    logger.log_choices(choices)
    print()

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
        print()

        story, choice_block = storyteller.generate_turn(
            state.history, choice.choice_description, success, intent, state.narrative
        )
        choices = choice_block.choices

        turn.ai = story.condensed
        state.record_turn(story.full, turn)

        logger.log_story(story.full)
        print()
        logger.log_state(state)
        print()

        if story.is_ending:
            if not (
                state.narrative.act == Act.RESOLUTION
                and state.narrative.progress >= 0.85
            ):
                raise RuntimeError('LLM attempted early ending')
            else:
                print('Story Ending')

            logger.log_story_end(
                act=state.narrative.act,
                progress=state.narrative.progress,
            )
            break

        logger.log_choices(choice_block.choices)
        print()

        allow_ending = (
            state.narrative.act == Act.RESOLUTION and state.narrative.progress >= 0.85
        )

        logger.log_narrative_state(
            act=state.narrative.act,
            progress=state.narrative.progress,
            allow_ending=allow_ending,
        )
        print()

        from_act = state.narrative.act

        advance_narrative(state.narrative, success)

        to_act = state.narrative.act

        if from_act != to_act:
            logger.log_narrative_transition(
                from_act=from_act,
                to_act=to_act,
            )
            print()

        allow_ending = (
            state.narrative.act == Act.RESOLUTION and state.narrative.progress >= 0.85
        )

        logger.log_narrative_state(
            act=state.narrative.act,
            progress=state.narrative.progress,
            allow_ending=allow_ending,
        )
        print()

    uploader.output_to_file(state.story, state.history, MODEL)


if __name__ == '__main__':
    main()
