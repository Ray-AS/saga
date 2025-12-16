import os

from backend.utils.configs import MODEL
from backend.utils.models import (
    CONDENSED_FORMAT,
    CondensedResponse,
    SystemMessageContent,
    Turn,
)
from groq import Groq
from groq.types.chat import ChatCompletionMessageParam as Message

# from backend.utils.test_values import mock_responses, test_history, test_start


class Storyteller:
    def __init__(self):
        self.client = Groq(
            api_key=os.environ.get('GROQ_API_KEY'),
        )

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

        self.format: str = CONDENSED_FORMAT

    def generate_start(self) -> CondensedResponse:
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    'role': 'system',
                    'content': f'Generate the start to a random fantasy D&D story that you will be the dungeon master to\n{self.format}',
                }
            ],
            model=MODEL,
        )

        raw = chat_completion.choices[0].message.content
        if not raw:
            raise Exception('Groq response is empty')

        response = CondensedResponse.model_validate_json(raw)
        return response

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

    def generate_context_messages(
        self, history: list[Turn], limit: int = -1
    ) -> list[Message]:
        length = len(history)

        # Determine how many turns to return
        if limit == -1 or limit > length:
            limit = length

        context_messages: list[Message] = []

        # For each turn, generate the user and ai action messages and append to context list
        for i in range(length - limit, length):
            user_message: Message = {
                'role': 'user',
                'content': f'Turn {i + 1}: {history[i]["user"]}',
            }
            assistant_message: Message = {
                'role': 'assistant',
                'content': f'Turn {i + 1}: {history[i]["ai"]}',
            }
            context_messages.append(user_message)
            context_messages.append(assistant_message)

        return context_messages

    def generate_outcome(
        self, history: list[Turn], player_action: str | None = None
    ) -> tuple[list[Message], CondensedResponse]:
        # Assemble whole message: system, context, user choice
        messages = [self.generate_system_message()] + self.generate_context_messages(
            history
        )

        if player_action:
            messages.append({'role': 'user', 'content': f'Choice: {player_action}'})

        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=MODEL,
        )

        raw = chat_completion.choices[0].message.content

        if not raw:
            raise Exception('Groq response is empty')

        response = CondensedResponse.model_validate_json(raw)
        return (messages, response)


# storyteller = Storyteller()
# storyteller.generate_start()
# storyteller.history = test_history
# outcome = storyteller.generate_outcome('escort the captives back to town')
# logger.pretty_print_json(outcome[0])
# logger.pretty_print_json(outcome[1])
