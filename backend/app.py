from backend.adapters.web import WebAdapter
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
