# import json

from pydantic import BaseModel, ValidationError


def parse_or_repair(raw: str, model: type[BaseModel]):
    try:
        return model.model_validate_json(raw)
    except ValidationError:
        start = raw.find('{')
        end = raw.rfind('}') + 1
        cleaned = raw[start:end]
        return model.model_validate_json(cleaned)
