import os

from dotenv import load_dotenv
from groq import Groq
from groq.types.chat import ChatCompletionMessageParam as Message

load_dotenv('backend/.env')

API_KEY = os.environ['GROQ_API_KEY']


class LLMClient:
    def __init__(self):
        self.client = Groq(api_key=API_KEY)

    def chat(self, messages: list[Message], model: str):
        return (
            self.client.chat.completions.create(model=model, messages=messages)
            .choices[0]
            .message.content
        )
