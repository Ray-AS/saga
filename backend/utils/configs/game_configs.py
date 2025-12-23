from backend.utils.models.game_models import Difficulty, Intent, Success

INITIAL_STAT_COUNT = 4
STAT_PROGRESS_LIMIT = 8

DC = {
    Difficulty.EASY: 6,
    Difficulty.MEDIUM: 10,
    Difficulty.HARD: 14,
    Difficulty.EXTREME: 18,
}

INTENT = {
    Intent.CAREFUL: 2,
    Intent.STANDARD: 0,
    Intent.BOLD: -2,
    Intent.DESPERATE: -4,
}

PROGRESS_VALUES = {
    Success.C_FAIL: -1,
    Success.FAIL: 0,
    Success.PARTIAL: 0,
    Success.SUCCESS: 1,
    Success.C_SUCCESS: 2,
}
