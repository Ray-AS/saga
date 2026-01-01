from backend.adapters.web import WebAdapter
from backend.models.api import ChoiceInfo
from backend.utils.logger import logger
from fastapi import FastAPI

app = FastAPI()
adapter = WebAdapter()


@app.post('/game/start')
def start():
    response = adapter.start()
    logger.log_story(response.full)
    logger.log_choices(response.choices)
    return response


@app.post('/game/{id}/choose')
def advance(id: str, choice_info: ChoiceInfo):
    response = adapter.advance(id, choice_info)
    logger.log_story(response.full)
    logger.log_choices(response.choices)
    return response
