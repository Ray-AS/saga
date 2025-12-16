import json

from backend.utils.models import Turn


class Logger:
    def __init__(self):
        pass

    def log_story(self, story: str, turn: Turn):
        print('---STORY---')
        print(story)
        print('---TURN---')
        self.pretty_print_json(turn)

    def log_character_generated(self, name: str):
        print(f'CHARACTER CREATED (Name: {name})')

    def pretty_print_json(self, data):
        print(json.dumps(data, indent=4, ensure_ascii=False))


logger = Logger()
