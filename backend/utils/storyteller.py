from textwrap import dedent

from models import MessageTemplate, Turn
from test_values import test_history


class Storyteller:
    def __init__(self):
        self.role: str = 'You are the Dungeon Master of an interactive story.'

        self.style_constraints: list[str] = [
            'Keep responses concise, vivid, and actionable.',
            'Always reference the player character in the second person ("you").',
        ]
        self.action_constraints: list[str] = [
            '**NEVER** control the player character; only describe the consequences of their actions.',
            '**NEVER** output any text outside the requested JSON structure.',
        ]

        self.format: str = dedent("""
        Construct your response as a single, valid JSON object following this schema:
        {
            full (str): "entire description of events (150-250 words)",
            condensed (str): "short description of events; keep only essentials that affect future story logic (30-50 words)",
            key (str): "one sentence description of events (8-15 words)",
            characters (list[dict{"name": "Frodo", "action": "Threw ring into the fire."}]): "characters involved in the events and what they did"
            choices (list[str]): "available options for the player to proceed; must be unique and make sense for the narrative (e.g. ["option 1", "option 2"])"
        }
        """).strip()

        self.history: list[Turn] = []

    def generate_history(self, limit: int = -1):
        length = len(self.history)
        if limit == -1 or limit > length:
            limit = length

        history = ''
        for i in range(length - limit, length):
            history += (
                f'Turn {i + 1}:\n'
                f'- User: {self.history[i]["user"]}\n'
                f'- AI: {self.history[i]["ai"]}\n'
            )

        return history[:-1]

    def generate_message(self, player_action: str):
        style_constraints = '\n'.join(f'- {c}' for c in self.style_constraints)
        action_constraints = '\n'.join(f'- {c}' for c in self.action_constraints)
        history = self.generate_history()

        text = MessageTemplate.format(
            role=self.role,
            style_constraints=style_constraints,
            action_constraints=action_constraints,
            format=self.format,
            history=history,
            player_action=player_action,
        ).strip()

        return text


storyteller = Storyteller()
storyteller.history = test_history
print(storyteller.generate_message('escort the captives back to town'))
