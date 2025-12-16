import os
import random

from backend.utils.configs import MODEL_LIST
from backend.utils.models import (
    FORMAT,
    Response,
    SystemMessageContent,
    Turn,
)
from groq import Groq
from groq.types.chat import ChatCompletionMessageParam as Message
from pydantic import ValidationError


class Storyteller:
    def __init__(self):
        self.client = Groq(
            api_key=os.environ.get('GROQ_API_KEY'),
        )

        self.role: str = 'You are the story teller of an interactive story.'

        self.style_constraints: list[str] = [
            'Keep responses concise, vivid, and actionable.',
            'Always reference the player character in the second person ("you").',
            'Avoid abstract phrases like "dark energy" or "malevolent presence".',
            'Prefer concrete sensory descriptions (sound, texture, temperature).',
            'Use varied sentence length for pacing.',
            'End scenes with a clear outcome summary before transitioning. Example: “You escape the guards, but are now wanted.”',
            'Your response MUST begin with `{` and end with `}`. Do NOT include narration, labels, explanations, or prefixes outside the JSON object. If you include any text outside the JSON, the response is invalid.',
            'The `full` section should be an organic description of the story progression for the user (i.e. do not include any tl;dr or short summary at the end; just the story)',
            '**ENSURE** json is in correct format `{"full": "...", "condensed": "...", "choices": ["...", "..."]}`',
        ]
        self.action_constraints: list[str] = [
            '**NEVER** control the player character; only describe the consequences of their actions.',
            '**NEVER** output any text outside the requested JSON structure.',
            '**ENSURE** generated outcomes and choices are not **always** positive, but can be neutral or negative based on context and player decisions (i.e. be unbiased and realistic)',
            'Each scene must have a clear objective. Once the objective is achieved or failed, the scene must end and transition. Do not extend a scene indefinitely.',
            'If the player repeats the same type of action more than twice, the situation must change decisively (success, failure, or irreversible consequence).',
            'NPCs must have conflicting motivations and imperfect knowledge.',
            'Player actions must have tangible costs (e.g. magic is not "free")',
            'Major NPCs must have a persistent attitude toward the player (e.g. hostile, wary, cooperative). Actions must shift this attitude and affect future behavior.',
            'Each choice must meaningfully alter the world state. Avoid choices that lead to the same outcome with different wording.',
            'The world must advance even if the player hesitates. Delays increase danger or remove options.',
            'When presenting choices, describe only the immediate intent or approach of each option, NOT its result. Consequences may ONLY be described after the player commits to a choice.',
            '**NEVER** describe the outcomes to a choices the user has yet to make. Doing so is considered **FAILURE**.',
        ]

        self.format: str = FORMAT

    def request_story(self, messages: list[Message]):
        model = random.choice(MODEL_LIST)

        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=model,
        )

        raw = chat_completion.choices[0].message.content
        if not raw:
            raise Exception('Groq response is empty')

        raw = raw.strip()

        print(model)
        print(raw)

        try:
            return Response.model_validate_json(raw)
        except ValidationError:
            print('Response format invalid, sending dummy data')
            failed_response: Response = Response(
                full='failed', condensed='failed', choices=[]
            )

            return failed_response

    def generate_start(self) -> Response:
        message: list[Message] = [
            {
                'role': 'system',
                'content': f'Generate the start to a random choose your own adventure story (can be any genre)\n{self.format}',
            }
        ]

        return self.request_story(message)

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
    ) -> tuple[list[Message], Response]:
        # Assemble whole message: system, context, user choice
        messages = [self.generate_system_message()] + self.generate_context_messages(
            history
        )

        if player_action:
            messages.append({'role': 'user', 'content': f'Choice: {player_action}'})

        response = self.request_story(messages)
        return (messages, response)
