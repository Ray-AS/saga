from pydantic import BaseModel, ValidationError


def extract_first_json(text: str):
    depth = 0
    start = None

    for i, ch in enumerate(text):
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start is not None:
                return text[start : i + 1]

    raise ValueError('No complete JSON object found')


def parse_or_repair(raw: str, model: type[BaseModel]):
    if '{' not in raw or '}' not in raw:
        raise ValueError('LLM response contains no JSON object')

    try:
        return model.model_validate_json(raw)
    except ValidationError:
        extracted = extract_first_json(raw)
        return model.model_validate_json(extracted)
