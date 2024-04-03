from pydantic import BaseModel


class SuggestionForMeReqDto(BaseModel):
    keyword: list[str]
