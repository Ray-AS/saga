from backend.game.character import Character
from backend.models.game import Stat, Success

PROGRESS_VALUES = {
    Success.C_FAIL: -1,
    Success.FAIL: 0,
    Success.PARTIAL: 0,
    Success.SUCCESS: 1,
    Success.C_SUCCESS: 2,
}

STAT_PROGRESS_LIMIT = 8


def apply_stat_progress(character: Character, stat: Stat, success: Success):
    character.stat_progress[stat] += PROGRESS_VALUES[success]
    if character.stat_progress[stat] >= STAT_PROGRESS_LIMIT:
        setattr(character.stats, stat.value, getattr(character.stats, stat.value) + 1)
        character.stat_progress[stat] -= STAT_PROGRESS_LIMIT
    elif character.stat_progress[stat] < 0:
        character.stat_progress[stat] = 0
