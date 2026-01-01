from backend.adapters.web import WebAdapter
from backend.database.db import Base, SessionLocal, engine
from backend.game.state import PlaythroughState
from backend.models.api import ChoiceInfo
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_adapter(db: Session = Depends(get_db)):
    return WebAdapter(db)


@app.get('/game')
def list_playthroughs(adapter: WebAdapter = Depends(get_adapter)):
    adapter.load_all_states()

    response = {'playthroughs': []}
    for id in adapter.states.keys():
        response['playthroughs'].append(
            {
                'playthrough_id': id,
                'act': adapter.states[id].narrative.act.name,
                'progress': adapter.states[id].narrative.progress,
                'can_end': adapter.states[id].narrative.allow_ending,
                'summary': adapter.storyteller.summarize_story(
                    adapter.states[id].history
                ),
            }
        )
    return response


@app.post('/game/start')
def start_story(adapter: WebAdapter = Depends(get_adapter)):
    response = adapter.start()
    return response


@app.post('/game/{id}/choose')
def advance_story(
    id: str, choice_info: ChoiceInfo, adapter: WebAdapter = Depends(get_adapter)
):
    response = adapter.advance(id, choice_info)
    return response


@app.get('/game/{id}')
def get_playthrough(id: str, adapter: WebAdapter = Depends(get_adapter)):
    state = adapter.get_state(id)

    return {
        'playthrough_id': id,
        'full': state.story[-1] if state.story else '',
        'condensed': state.history[-1].ai if state.history else '',
        'choices': state.current_choices,
    }


@app.delete('/game/{id}')
def delete_playthrough(id: str, adapter: WebAdapter = Depends(get_adapter)):
    response = adapter.uploader.delete(id)
    if response:
        return {
            'message': f'{id}.json successfully deleted.',
        }
    return {
        'message': f'{id}.json not found.',
    }
