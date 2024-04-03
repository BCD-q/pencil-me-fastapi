from fastapi import APIRouter, Query, Body
from typing import Annotated, Optional
from pydantic import BaseModel
from datetime import datetime


class LanguageReqDto(BaseModel):
    memberId: int
    memberName: Annotated[str, Query(max_length=10)] = ...
    memberEmail: Annotated[str, Query(pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$")] = ...
    memberStatement: Annotated[str, Query(min_length=15, max_length=200)] = ...
    requestedDate: str = ...


class LanguageResDto(BaseModel):
    memberId: int
    categoryId: int
    title: str
    contents: Optional[str] = None
    deadline: datetime


class LanguageResDtoDescription(BaseModel):
    memberId: str
    categoryId: str
    title: str
    contents: str
    deadline: str