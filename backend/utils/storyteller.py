import os

from backend.utils.configs.storyteller_configs import (
    ACTION_CONSTRAINTS,
    FORMAT,
    MODEL_LIST,
    PROGRESSION_DESCRIPTION,
    ROLE_DESCRIPTION,
    STARTING_PROMPT,
    STYLE_CONSTRAINTS,
)
from backend.utils.models.playthrough_models import Turn
from backend.utils.models.storyteller_models import (
    Response,
    StoryOutcome,
    SystemMessageContent,
)
from groq import Groq
from groq.types.chat import ChatCompletionMessageParam as Message
from pydantic import ValidationError


class Storyteller:
    """
    Represents dynamic story generator for an interactive game

    Attributes:
        client (Groq, static): LLM model that generates story
        role (str): describes role of the LLM
        style_constraints (list[str]): stylistic rules LLM must follow
        action_constraints (list[str]): action rules LLM must follow
        format (str): schema which LLM response must match
    """

    client = Groq(
        api_key=os.environ.get('GROQ_API_KEY'),
    )

    def __init__(self):
        self.role = ROLE_DESCRIPTION
        self.style_constraints = STYLE_CONSTRAINTS
        self.action_constraints = ACTION_CONSTRAINTS
        self.format = FORMAT
        self.progression_description = PROGRESSION_DESCRIPTION

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
            failed_response = Response(full='failed', condensed='failed', choices=[])

            return failed_response

    def generate_start(self) -> Response:
        """
        Generates opening sequence of story

        Returns:
            Response: structure containing opening paragraph(s) and choices
        """
        message = [
            self.generate_system_message(),
            STARTING_PROMPT,
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
            progression_description=self.progression_description,
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
                'content': f'Turn {i + 1}: {history[i].user}',
            }
            assistant_message: Message = {
                'role': 'assistant',
                'content': history[i].ai,
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
            StoryOutcome: assembled messages; response model containing advancement details
        """
        # Assemble whole message: system, context, user choice
        messages = [self.generate_system_message()] + self.generate_context_messages(
            history
        )

        if player_action:
            messages.append({'role': 'user', 'content': f'Choice: {player_action}'})

        response = self.request_story(messages)
        return StoryOutcome(messages=messages, response=response)
