from sqlalchemy.orm import Session

from backend.models.data_models import (
    Character,
    Choice,
    GameSession,
    HistoryEntry,
    StoryEntry,
)


class DBUploader:
    def __init__(self, db: Session):
        self.db = db

    # get all available session ids
    def list_ids(self):
        sessions = self.db.query(GameSession.id).all()
        session_ids = [str(s.id) for s in sessions]
        return session_ids

    def save(self, state: dict, session_id: str = ''):
        character_data = state['character']

        if session_id != '':
            game_session = (
                self.db.query(GameSession).filter_by(id=int(session_id)).first()
            )

            if game_session is None:
                raise ValueError('Session does not exist')

            character = game_session.character
            character.name = character_data['name']
            character.stats = character_data['stats']
            character.stat_progress = character_data['stat_progress']
        else:
            # generate new character if no session id provided
            character = Character(
                name=character_data['name'],
                stats=character_data['stats'],
                stat_progress=character_data['stat_progress'],
            )

            self.db.add(character)
            # stage changes
            self.db.flush()

            game_session = GameSession(
                act=state['narrative']['act'],
                progress=state['narrative']['progress'],
                character_id=character.id,
            )

            self.db.add(game_session)
            # stage changes
            self.db.flush()

            session_id = str(game_session.id)

        # delete old data to prepare for replacement
        self.db.query(StoryEntry).filter_by(session_id=game_session.id).delete()
        self.db.query(Choice).filter_by(session_id=game_session.id).delete()
        self.db.query(HistoryEntry).filter_by(session_id=game_session.id).delete()

        # repopulate all session data using current state of playthrough
        # repopulate story data
        for i, s in enumerate(state['story']):
            self.db.add(StoryEntry(session_id=game_session.id, text=s, order=i))

        # repopulate choice data
        for c in state['choices']:
            self.db.add(
                Choice(
                    session_id=game_session.id,
                    description=c['choice_description'],
                    difficulty=c['difficulty'],
                    type=c['type'],
                )
            )

        # repopulate turn data
        for i, h in enumerate(state['history']):
            self.db.add(
                HistoryEntry(
                    session_id=game_session.id, user=h['user'], ai=h['ai'], order=i
                )
            )

        # repopulate narrative data
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
