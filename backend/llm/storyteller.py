from textwrap import dedent

from backend.llm.client import LLMClient
from backend.llm.prompts.act import ACT_GUIDELINES
from backend.llm.prompts.choices import CHOICE_PROMPT
from backend.llm.prompts.story import STORY_PROMPT_START, STORY_PROMPT_TURN
from backend.llm.prompts.system import SYSTEM_PROMPT
from backend.llm.validation import parse_or_repair
from backend.models.game import Act, NarrativeState, Success, Turn
from backend.models.llm import ChoiceResponse, StoryResponse
from groq.types.chat import ChatCompletionMessageParam as Message

MODEL_LIST = [
    'llama-3.3-70b-versatile',
    'openai/gpt-oss-120b',
]
MODEL = MODEL_LIST[0]


class Storyteller:
    def __init__(self):
        self.client = LLMClient()

    def generate_start(self) -> tuple[StoryResponse, ChoiceResponse]:
        messages: list[Message] = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {
                'role': 'user',
                'content': STORY_PROMPT_START,
            },
        ]

        story_raw = self.client.chat(messages, MODEL)

        if not story_raw:
            raise ValueError('LLM did not provide story response')

        story = StoryResponse.model_validate(parse_or_repair(story_raw, StoryResponse))

        choices_raw = self.client.chat(
            messages
            + [{'role': 'assistant', 'content': f'NEW STORY: {story.condensed}'}]
            + [{'role': 'user', 'content': CHOICE_PROMPT}],
            MODEL,
        )

        if not choices_raw:
            raise ValueError('LLM did not provide choice response')

        choices = ChoiceResponse.model_validate(
            parse_or_repair(choices_raw, ChoiceResponse)
        )

        return story, choices

    def generate_turn(
        self,
        history: list[Turn],
        action: str,
        success: Success,
        intent: str,
        narrative: NarrativeState,
    ) -> tuple[StoryResponse, ChoiceResponse]:
        guidelines = ACT_GUIDELINES[narrative.act]
        allow_ending = narrative.act == Act.RESOLUTION and narrative.progress >= 0.85

        if allow_ending:
            ending_rule = 'You **MAY** conclude the story in a satisfying final ending.'
        else:
            ending_rule = 'You **MUST** continue the story and NOT conclude it yet.'

        messages: list[Message] = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {
                'role': 'system',
                'content': dedent(f"""
                Act: {narrative.act.name}
                Act Progress: {narrative.progress:.2f}

                Tone: {guidelines['tone']}
                Focus: {guidelines['focus']}
                Rule: {guidelines['rule']}
                Ending rule: {ending_rule}
                """),
            },
        ]

        for t in history:
            messages.append({'role': 'user', 'content': t.user})
            messages.append({'role': 'assistant', 'content': t.ai})

        story_raw = self.client.chat(
            messages
            + [
                {
                    'role': 'user',
                    'content': STORY_PROMPT_TURN.format(
                        action=action,
                        success=success.value,
                        intent=intent,
                    ),
                }
            ],
            MODEL,
        )

        if not story_raw:
            raise ValueError('LLM did not provide story response')

        story = StoryResponse.model_validate(parse_or_repair(story_raw, StoryResponse))

        choices_raw = self.client.chat(
            messages
            + [{'role': 'assistant', 'content': f'NEW STORY: {story.condensed}'}]
            + [{'role': 'user', 'content': CHOICE_PROMPT}],
            MODEL,
        )

        if not choices_raw:
            raise ValueError('LLM did not provide choice response')

        choices = ChoiceResponse.model_validate(
            parse_or_repair(choices_raw, ChoiceResponse)
        )

        return story, choices
