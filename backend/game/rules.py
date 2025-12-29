import random

from backend.models.game import Success


def roll_d20() -> int:
    return random.randint(1, 20)


def determine_success(
    roll: int,
    total: int,
    dc: int,
) -> Success:
    if roll == 1:
        return Success.C_FAIL
    if roll == 20:
        return Success.C_SUCCESS
    if total < dc - 2:
        return Success.FAIL
    if total > dc + 2:
        return Success.SUCCESS
    return Success.PARTIAL
