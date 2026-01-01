from backend.adapters.web import WebAdapter
from backend.game.state import PlaythroughState
from backend.models.api import ChoiceInfo
from fastapi import FastAPI

app = FastAPI()
adapter = WebAdapter()


@app.get('/game')
def list_playthroughs():
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
def start_story():
    response = adapter.start()
    return response


@app.post('/game/{id}/choose')
def advance_story(id: str, choice_info: ChoiceInfo):
    response = adapter.advance(id, choice_info)
    return response


@app.get('/game/{id}')
def get_playthrough(id: str):
    if id not in adapter.states:
        data = adapter.uploader.load(id)
        adapter.states[id] = PlaythroughState.from_dict(data)

    state = adapter.states[id]
    return {
        'playthrough_id': id,
        'full': state.story[-1] if state.story else '',
        'condensed': state.history[-1].ai if state.history else '',
        'choices': state.current_choices,
    }


@app.delete('/game/{id}')
def delete_playthrough(id: str):
    response = adapter.uploader.delete(id + '.json')
    if response:
        return {
            'message': f'{id}.json successfully deleted.',
        }
    return {
        'message': f'{id}.json not found.',
    }
