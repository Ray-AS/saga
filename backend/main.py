import os

from backend.utils.configs import MODEL
from groq import Groq


def main():
    # client = Groq(
    #     api_key=os.environ.get('GROQ_API_KEY'),
    # )

    # chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             'role': 'user',
    #             'content': 'Explain the importance of fast language models',
    #         }
    #     ],
    #     model=MODEL,
    # )

    # print(chat_completion.choices[0].message.content)
    pass


if __name__ == '__main__':
    main()
