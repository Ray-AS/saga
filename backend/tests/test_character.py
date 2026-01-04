from backend.game.character import Character
from backend.models.game import Stat


def test_character_name_is_set():
    character = Character(name='Hero')
    assert character.name == 'Hero'


def test_character_default_name_is_empty():
    character = Character()
    assert character.name == ''


def test_character_starts_with_stats():
    character = Character()
    assert character.stats is not None


def test_character_stat_progress_starts_at_zero():
    character = Character()
    for stat in Stat:
        assert character.stat_progress[stat] == 0
        assert getattr(character.stats, stat.name.lower()) == 0
