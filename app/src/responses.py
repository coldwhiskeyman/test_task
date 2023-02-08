from pydantic import BaseModel


class InvalidGender(BaseModel):
    detail: str = 'Invalid gender'
