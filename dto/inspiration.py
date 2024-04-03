from pydantic import BaseModel


class SuggestionForMeReqDto(BaseModel):
    keyword: list[str]


class SuggestionForMeResDto(BaseModel):
    title: str
    link: str
    thumbnail_url: str


class SuggestionOfTheDayDto(BaseModel):
    title: str
    link: str
    thumbnail_url: str
