class Storyteller:
    def __init__(self):
        self.system_prompt: str = (
            'You are the Dungeon Master of an interactive story.'
            'Keep responses concise, vivid, and actionable.'
            'Never control the player character; only describe outcomes.'
        )

        self.history = []
