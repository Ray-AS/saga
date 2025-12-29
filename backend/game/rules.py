import random

from backend.models.game import Difficulty, Success

DC = {
    Difficulty.EASY: 6,
    Difficulty.MEDIUM: 10,
    Difficulty.HARD: 14,
    Difficulty.EXTREME: 18,
}


def roll_d20() -> int:
    return random.randint(1, 20)


def determine_success(
    roll: int,
    total: int,
    dc: Difficulty,
) -> Success:
    if roll == 1:
        return Success.C_FAIL
    if roll == 20:
        return Success.C_SUCCESS
    if total < DC[dc] - 2:
        return Success.FAIL
    if total > DC[dc] + 2:
        return Success.SUCCESS
    return Success.PARTIAL
