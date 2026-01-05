import pytest

from backend.game.narrative_progression import advance_narrative
from backend.models.game import Act, NarrativeState, Success


@pytest.mark.parametrize('success', list(Success))
def test_narrative_progress_increases_for_any_success(success):
    narrative = NarrativeState(progress=0.0)
    advance_narrative(narrative, success)
    assert narrative.progress > 0.0


def test_act_change_to_escalation():
    narrative = NarrativeState(progress=0.9)
    advance_narrative(narrative, Success.SUCCESS)
    assert narrative.act == Act.ESCALATION
    assert narrative.progress == 0.0


def test_act_change_to_resolution():
    narrative = NarrativeState(act=Act.ESCALATION, progress=0.9)
    advance_narrative(narrative, Success.SUCCESS)
    assert narrative.act == Act.RESOLUTION
    assert narrative.progress == 0.0


def test_progress_does_not_exceed_threshold():
    narrative = NarrativeState(act=Act.RESOLUTION, progress=1.0)
    advance_narrative(narrative, Success.SUCCESS)
    assert narrative.act == Act.RESOLUTION
    assert narrative.progress == 1.0
