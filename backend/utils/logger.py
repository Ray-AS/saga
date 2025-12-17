import json

from backend.utils.models import Turn


class Logger:
    def __init__(self):
        pass

    def log_story(self, story: str, turn: Turn):
        print('---STORY---')
        print(story)
        print('---TURN---')
        print(turn.model_dump_json(indent=4))

    def log_character_generated(self, name: str):
        print(f'CHARACTER CREATED (Name: {name})')

    def pretty_print_json(self, data):
        print(json.dumps(data, indent=4, ensure_ascii=False))


logger = Logger()
