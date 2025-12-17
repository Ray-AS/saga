import os

from backend.utils.configs import MODEL_LIST
from backend.utils.models import (
    FORMAT,
    PROGRESSION_DESCRIPTION,
    Response,
    StoryOutcome,
    SystemMessageContent,
    Turn,
)
from groq import Groq
from groq.types.chat import ChatCompletionMessageParam as Message
from pydantic import ValidationError


class Storyteller:
    """
    Represents dynamic story generator for an interactive game

    Attributes:
        client (Groq): LLM model that generates story
        role (str): describes role of the LLM
        style_constraints (list[str]): stylistic rules LLM must follow
        action_constraints (list[str]): action rules LLM must follow
        format (str): schema which LLM response must match
    """

    def __init__(self):
        self.client = Groq(
            api_key=os.environ.get('GROQ_API_KEY'),
        )

        self.role: str = 'You are the story teller of an interactive story.'

        self.style_constraints = [
            'Output strictly valid JSON in the exact format matching the schema: {"full": "...", "condensed": "...", "choices": ["..."]}. No text before or after the JSON object',
            "The response must begin with '{' and end with '}'. Do not include any text outside the JSON object.",
            'Escape double quotes with a backslash if they appear inside a string.',
            'DO NOT include a "choices: ..." section in the "full" value of the object.',
            "Write exclusively in second person, always referring to the player as 'you'.",
            "The 'full' field must contain only immersive narrative prose. Do not include summaries, labels, or meta commentary.",
            'Use concrete sensory details (sound, texture, temperature, smell) instead of abstract or vague concepts.',
            "Avoid generic fantasy phrases (e.g., 'dark energy', 'malevolent presence', 'ancient power').",
            'Keep prose vivid, concise, and actionable; every paragraph should move the situation forward.',
            'Vary sentence length intentionally to control pacing and tension.',
            'End each scene with a clear, natural consequence embedded in the narrative (not a labeled summary).',
            "Do not summarize consequences using labels like 'Outcome:' or 'Result:'. Consequences must be embedded naturally in the narrative.",
        ]

        self.action_constraints = [
            "Never control the player character. Describe only the consequences of the player's chosen action.",
            'If you accidentally violate player agency or describe unchosen outcomes, you MUST immediately rewrite the response to fix the issue before replying.'
            'Ensure outcomes are unbiased and realistic. Success is not guaranteed; failure and neutral results must occur when justified.',
            'Every scene must have a clear objective. Once it is achieved or failed, end the scene and transition.',
            'If the player repeats the same type of action more than twice, force a decisive change (success, failure, or irreversible consequence).',
            'NPCs must have conflicting motivations, limited knowledge, and persistent attitudes that change based on player actions.',
            'All player actions must have tangible costs or tradeoffs (time, resources, injury, reputation, risk).',
            'Each choice must meaningfully change the world state. Do not offer choices that lead to the same result.',
            'The world advances even if the player hesitates. Delays increase danger, remove options, or worsen outcomes.',
            'When presenting choices, describe only the immediate intent or approach. Never reveal results in advance.',
            'Never describe the consequences of an unchosen option. Consequences are revealed only after the player commits.',
            "After resolving the player's chosen action, stop. Do not advance the story beyond the immediate consequences.",
        ]

        self.format: str = FORMAT

    def request_story(self, messages: list[Message]) -> Response:
        """
        Requests next portion of story from LLM based on prior turn history

        Args:
            messages (list[Message]): system prompt; user actions and ai reactions per turn

        Raises:
            ValidationError: generated response does not match Pydantic Response model

        Returns:
            Response: structure containing story progression and choices
        """
        model = MODEL_LIST[1]
        print(model)

        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=model,
        )

        raw = chat_completion.choices[0].message.content
        if not raw:
            raise Exception('Groq response is empty')

        raw = raw.strip()

        try:
            return Response.model_validate_json(raw)
        except ValidationError:
            print('Response format invalid, sending dummy data')
            failed_response: Response = Response(
                full='failed', condensed='failed', choices=[]
            )

            return failed_response

    def generate_start(self) -> Response:
        """
        Generates opening sequence of story

        Returns:
            Response: structure containing opening paragraph(s) and choices
        """
        message: list[Message] = [
            self.generate_system_message(),
            {
                'role': 'user',
                'content': 'Generate the opening scene of a new interactive story.',
            },
        ]

        return self.request_story(message)

    def generate_system_message(self) -> Message:
        """
        Generates system prompt by combining attributes

        Returns:
            Message: dict containing system info that matches the message model expected by LLM
        """
        # Join and format constraints
        style_constraints = '\n'.join(f'- {c}' for c in self.style_constraints)
        action_constraints = '\n'.join(f'- {c}' for c in self.action_constraints)

        # Assemble message content using template
        system_message_content = SystemMessageContent.format(
            role=self.role,
            style_constraints=style_constraints,
            action_constraints=action_constraints,
            progression_description=PROGRESSION_DESCRIPTION,
            format=self.format,
        ).strip()

        return {
            'role': 'system',
            'content': system_message_content,
        }

    def generate_context_messages(
        self, history: list[Turn], limit: int = -1
    ) -> list[Message]:
        """
        Generates context prompt by combining turn history of user and ai

        Args:
            history (list[Turn]): turn history for a playthrough
            limit (int, optional): number of turns to include in prompt. Defaults to -1.

        Returns:
            list[Message]: list of dicts containing turn info that matches the message model expected by LLM
        """
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
                'content': history[i]['ai'],
            }
            context_messages.append(user_message)
            context_messages.append(assistant_message)

        return context_messages

    def generate_outcome(
        self, history: list[Turn], player_action: str | None = None
    ) -> StoryOutcome:
        """
        Combines system and context messages into one to generate story advancement

        Args:
            history (list[Turn]): turn history for a playthrough
            player_action (str | None, optional): choice player makes for given choices. Defaults to None.

        Returns:
            tuple[list[Message], Response]: assembled messages; response model containing advancement details
        """
        # Assemble whole message: system, context, user choice
        messages = [self.generate_system_message()] + self.generate_context_messages(
            history
        )

        if player_action:
            messages.append({'role': 'user', 'content': f'Choice: {player_action}'})

        response = self.request_story(messages)
        return StoryOutcome(messages=messages, response=response)
