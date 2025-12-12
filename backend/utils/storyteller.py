import json
import os
import random
from textwrap import dedent

from configs import MODEL
from groq import Groq
from groq.types.chat import ChatCompletionMessageParam as Message
from logger import logger
from models import SystemMessageContent, Turn
from test_values import mock_responses, test_history


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
            '**ENSURE** generated outcomes and choices are not **always** positive, but can be neutral or negative based on context and player decisions (i.e. be unbiased and realistic)',
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

    def generate_system_message(self) -> Message:
        # Join and format constraints
        style_constraints = '\n'.join(f'- {c}' for c in self.style_constraints)
        action_constraints = '\n'.join(f'- {c}' for c in self.action_constraints)

        # Assemble message content using template
        system_message_content = SystemMessageContent.format(
            role=self.role,
            style_constraints=style_constraints,
            action_constraints=action_constraints,
            format=self.format,
        ).strip()

        return {
            'role': 'system',
            'content': system_message_content,
        }

    def generate_context_messages(self, limit: int = -1):
        length = len(self.history)

        # Determine how many turns to return
        if limit == -1 or limit > length:
            limit = length

        context_messages: list[Message] = []

        # For each turn, generate the user and ai action messages and append to context list
        for i in range(length - limit, length):
            user_message: Message = {
                'role': 'user',
                'content': f'Turn {i + 1}: {self.history[i]["user"]}',
            }
            assistant_message: Message = {
                'role': 'assistant',
                'content': f'Turn {i + 1}: {self.history[i]["ai"]}',
            }
            context_messages.append(user_message)
            context_messages.append(assistant_message)

        return context_messages

    def generate_outcome(self, player_action: str):
        # Assemble whole message: system, context, user choice
        messages = [self.generate_system_message()] + self.generate_context_messages()
        messages.append({'role': 'user', 'content': f'Choice: {player_action}'})

        # client = Groq(
        #     api_key=os.environ.get('GROQ_API_KEY'),
        # )

        # chat_completion = client.chat.completions.create(
        #     messages=messages,
        #     model=MODEL,
        # )

        # actual_response = chat_completion.choices[0].message.content

        # Return a mock response for now
        return [messages, random.choice(mock_responses)]


# storyteller = Storyteller()
# storyteller.history = test_history
# outcome = storyteller.generate_outcome('escort the captives back to town')
# logger.pretty_print_json(outcome[0])
# logger.pretty_print_json(outcome[1])
