from backend.game.progression import apply_stat_progress
from backend.game.rules import determine_success, roll_d20
from backend.game.state import PlaythroughState
from backend.models.game import Choice, Turn


class GameEngine:
    def resolve_turn(self, state: PlaythroughState, choice: Choice, intent_mod, dc):
        roll = roll_d20()
        stat = getattr(state.character.stats, choice.type.value)
        total = roll + stat + intent_mod

        success = determine_success(roll, total, dc)
        apply_stat_progress(state.character, choice.type, success)

        turn = Turn(user=f'{choice.choice_description} [{success.value}]', ai='')

        return success, turn
