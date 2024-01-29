from pydantic import BaseModel


class CommonResDto(BaseModel):
    msg: str
    result: dict = {}
