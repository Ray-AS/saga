from backend.models.game import Act

ACT_GUIDELINES = {
    Act.SETUP: {
        'tone': 'mysterious, exploratory',
        'focus': 'introducing factions, locations, and stakes',
        'rule': 'Do NOT resolve major conflicts.',
    },
    Act.ESCALATION: {
        'tone': 'tense, dangerous',
        'focus': 'complications, betrayals, revelations',
        'rule': 'Raise stakes but avoid final resolution.',
    },
    Act.RESOLUTION: {
        'tone': 'decisive, emotional',
        'focus': 'consequences, closure, payoff',
        'rule': 'Resolve the central conflict and conclude the story.',
    },
}
