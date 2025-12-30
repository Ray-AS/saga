from datetime import datetime
from pathlib import Path

from backend.models.game import Turn


class FileUploader:
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
