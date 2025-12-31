from backend.adapters.web import WebAdapter
from backend.utils.logger import logger
from fastapi import FastAPI

app = FastAPI()
adapter = WebAdapter()


@app.get('/')
def index():
    response = adapter.start()
    logger.log_story(response.full)
    logger.log_choices(response.choices)
    return response
