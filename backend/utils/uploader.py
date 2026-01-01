import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from backend.models.game import Turn


class FileUploader:
    def __init__(self) -> None:
        self.db_dir = Path(__file__).parent.parent / 'data'
        self.db_dir.mkdir(parents=True, exist_ok=True)

    def generate_story_summary(self, story: list[str]):
        complete_story = '---STORY SUMMARY---\n' + '\n\n'.join(story)
        return complete_story

    def generate_turn_summary(self, history: list[Turn]):
        lines: list[str] = []

        for i, turn in enumerate(history, start=1):
            lines.append(f'[TURN {i}]')
            lines.append('YOU:')
            lines.append(turn.user or '[no action]')
            lines.append('')
            lines.append('AI:')
            lines.append(turn.ai)
            lines.append('')

        return '---TURN SUMMARY---\n' + '\n'.join(lines).strip()

    def output_to_file(self, story: list[str], history: list[Turn], model: str):
        story_output = self.generate_story_summary(story)
        turn_output = self.generate_turn_summary(history)

        model = model.replace('/', '_')
        filename = f'{model}_'

        current_datetime = datetime.now()
        timestamp_str = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
        filename += timestamp_str

        script_dir = Path(__file__).parent
        filepath = script_dir.parent / 'playthroughs' / f'{filename}.txt'

        with open(filepath, 'w') as f:
            f.write(story_output)
            f.write('\n\n')
            f.write(turn_output)

    def save(self, data: dict, playthrough_id: str = ''):
        if playthrough_id == '':
            playthrough_id = str(uuid4())
        filepath = self.db_dir / f'{playthrough_id}.json'
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return playthrough_id

    def load(self, playthrough_id: str):
        filepath = self.db_dir / f'{playthrough_id}.json'
        with open(filepath, 'r') as f:
            return json.load(f)

    def delete(self, filename: str):
        if '.json' not in filename:
            raise ValueError('File not a .json file')

        filepath = self.db_dir / filename

        if filepath.is_file():
            filepath.unlink()
            return True
        else:
            return False
