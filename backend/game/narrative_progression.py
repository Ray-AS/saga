from backend.models.game import Act, NarrativeState, Success

PROGRESS_SPEEDS = {
    'slow': {
        Success.C_FAIL: 0.00,
        Success.FAIL: 0.05,
        Success.PARTIAL: 0.1,
        Success.SUCCESS: 0.15,
        Success.C_SUCCESS: 0.2,
    },
    'medium': {
        Success.C_FAIL: 0.5,
        Success.FAIL: 0.1,
        Success.PARTIAL: 0.15,
        Success.SUCCESS: 0.2,
        Success.C_SUCCESS: 0.3,
    },
    'fast': {
        Success.C_FAIL: 0.15,
        Success.FAIL: 0.2,
        Success.PARTIAL: 0.25,
        Success.SUCCESS: 0.3,
        Success.C_SUCCESS: 0.4,
    },
    'lightning': {
        Success.C_FAIL: 0.3,
        Success.FAIL: 0.4,
        Success.PARTIAL: 0.5,
        Success.SUCCESS: 0.6,
        Success.C_SUCCESS: 0.7,
    },
}

PROGRESS_DELTA = PROGRESS_SPEEDS['lightning']


def advance_narrative(narrative: NarrativeState, success: Success):
    narrative.progress += PROGRESS_DELTA[success]

    if narrative.progress > 1.0:
        narrative.progress = 1.0

    if narrative.progress >= 1.0 and narrative.act != Act.RESOLUTION:
        narrative.progress = 0.0
        narrative.act = Act(narrative.act.value + 1)
