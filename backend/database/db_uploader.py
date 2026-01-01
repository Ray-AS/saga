from backend.models.data_models import (
    Character,
    Choice,
    GameSession,
    HistoryEntry,
    StoryEntry,
)
from sqlalchemy.orm import Session


class DBUploader:
    def __init__(self, db: Session):
        self.db = db

    def list_ids(self):
        sessions = self.db.query(GameSession.id).all()
        ids = [str(s.id) for s in sessions]
        return ids

    def save(self, state: dict, session_id: str = ''):
        char_data = state['character']

        if session_id != '':
            game_session = (
                self.db.query(GameSession.id).filter_by(id=int(session_id)).first()
            )

            if game_session is None:
                raise ValueError('Session does not exist')

            character = game_session.character
            character.name = char_data['name']
            character.stats = char_data['stats']
            character.stat_progress = char_data['stat_progress']
        else:
            character = Character(
                name=char_data['name'],
                stats=char_data['stats'],
                stat_progress=char_data['stat_progress'],
            )

            self.db.add(character)
            self.db.flush()

            game_session = GameSession(
                act=state['narrative']['act'],
                progress=state['narrative']['progress'],
                character_id=character.id,
            )

            self.db.add(game_session)
            self.db.flush()

            session_id = str(game_session.id)

        self.db.query(StoryEntry).filter_by(session_id=game_session.id).delete()
        self.db.query(Choice).filter_by(session_id=game_session.id).delete()
        self.db.query(HistoryEntry).filter_by(session_id=game_session.id).delete()

        for i, s in enumerate(state['story']):
            self.db.add(StoryEntry(session_id=game_session.id, text=s, order=i))

        for c in state['choices']:
            self.db.add(
                Choice(
                    session_id=game_session.id,
                    description=c['choice_description'],
                    difficulty=c['difficulty'],
                    type=c['type'],
                )
            )

        for i, h in enumerate(state['history']):
            self.db.add(
                HistoryEntry(
                    session_id=game_session.id, user=h['user'], ai=h['ai'], order=i
                )
            )

        game_session.act = state['narrative']['act']
        game_session.progress = state['narrative']['progress']

        self.db.commit()
        return session_id

    def load(self, session_id: str):
        game_session = self.db.query(GameSession).filter_by(id=int(session_id)).first()

        if not game_session:
            raise ValueError('Session does not exist')

        story = [
            s.text for s in sorted(game_session.story_entries, key=lambda x: x.order)
        ]

        history = [
            {'user': h.user, 'ai': h.ai}
            for h in sorted(game_session.history_entries, key=lambda x: x.order)
        ]

        choices = [
            {
                'choice_description': c.description,
                'difficulty': c.difficulty,
                'type': c.type,
            }
            for c in game_session.choices
        ]

        character = {
            'name': game_session.character.name,
            'stats': game_session.character.stats,
            'stat_progress': game_session.character.stat_progress,
        }

        narrative = {'act': game_session.act, 'progress': game_session.progress}

        return {
            'story': story,
            'history': history,
            'choices': choices,
            'character': character,
            'narrative': narrative,
        }

    def delete(self, session_id: str):
        game_session = self.db.query(GameSession).filter_by(id=int(session_id)).first()

        if not game_session:
            return False

        self.db.delete(game_session)
        self.db.commit()

        return True
