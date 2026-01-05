import pytest

from backend.game.rules import PARTIAL_WINDOW, determine_success
from backend.models.game import Difficulty, Success

DIFFICULTY = 10
DC = Difficulty.MEDIUM


@pytest.mark.parametrize(
    'roll, total, dc, expected',
    [
        # Check criticals
        (1, 20, DC, Success.C_FAIL),
        (20, 1, DC, Success.C_SUCCESS),
        # Check regular
        (5, DIFFICULTY - PARTIAL_WINDOW - 1, DC, Success.FAIL),
        (5, DIFFICULTY - PARTIAL_WINDOW, DC, Success.PARTIAL),
        (5, DIFFICULTY, DC, Success.PARTIAL),
        (5, DIFFICULTY + PARTIAL_WINDOW, DC, Success.PARTIAL),
        (5, DIFFICULTY + PARTIAL_WINDOW + 1, DC, Success.SUCCESS),
    ],
)
def test_determine_success(roll, total, dc, expected):
    assert determine_success(roll, total, dc) == expected
