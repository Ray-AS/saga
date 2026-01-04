from backend.game.character import Character
from backend.game.engine import GameEngine
from backend.game.narrative_progression import advance_narrative
from backend.game.rules import determine_success
from backend.game.stat_progression import apply_stat_progress
from backend.game.state import PlaythroughState
from backend.models.game import Stat, Success


def test_character_creation():
    character = Character(name='Hero')
    another_character = Character()
    assert character.name == 'Hero'
    assert another_character.name == ''
    assert character.stats is not None
    for stat in Stat:
        assert stat in character.stat_progress
        assert character.stat_progress[stat] == 0
        assert getattr(character.stats, stat.name.lower()) == 0


def test_stat_progression():
    character = Character(name='Hero')
    initial_force = character.stats.force
    apply_stat_progress(character, Stat.FORCE, Success.SUCCESS)
    assert character.stat_progress[Stat.FORCE] == 1
    apply_stat_progress(character, Stat.FORCE, Success.C_SUCCESS)
    assert character.stat_progress[Stat.FORCE] == 3
    for _ in range(5):
        apply_stat_progress(character, Stat.FORCE, Success.SUCCESS)
    assert character.stats.force == initial_force + 1
    assert character.stat_progress[Stat.FORCE] == 0
