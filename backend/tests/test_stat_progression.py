import pytest

from backend.game.character import Character
from backend.game.stat_progression import (
    STAT_PROGRESS_LIMIT,
    apply_stat_progress,
)
from backend.models.game import Stat, Success


@pytest.mark.parametrize(
    'success,expected',
    [
        (Success.C_FAIL, 0),
        (Success.FAIL, 0),
        (Success.PARTIAL, 0),
        (Success.SUCCESS, 1),
        (Success.C_SUCCESS, 2),
    ],
)
def test_stat_changes_for_all_success_types(success, expected):
    character = Character()
    apply_stat_progress(character, Stat.FORCE, success)
    assert character.stat_progress[Stat.FORCE] == expected


@pytest.mark.parametrize('stat', list(Stat))
def test_stat_increases_when_threshold_reached(stat):
    character = Character()
    initial = getattr(character.stats, stat.name.lower())

    for _ in range(STAT_PROGRESS_LIMIT):
        apply_stat_progress(character, stat, Success.SUCCESS)

    assert getattr(character.stats, stat.name.lower()) == initial + 1
    assert character.stat_progress[stat] == 0
