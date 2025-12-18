from pydantic import BaseModel


class Turn(BaseModel):
    user: str
    ai: str
