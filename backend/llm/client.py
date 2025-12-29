import os

from groq import Groq
from groq.types.chat import ChatCompletionMessageParam as Message


class LLMClient:
    def __init__(self):
        self.client = Groq(api_key=os.environ['GROQ_API_KEY'])

    def chat(self, messages: list[Message], model: str):
        return (
            self.client.chat.completions.create(model=model, messages=messages)
            .choices[0]
            .message.content
        )
