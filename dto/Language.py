from fastapi import APIRouter, Query, Body
from typing import Annotated
from pydantic import BaseModel


class LanguageReqDto(BaseModel):
    userId: str = ...
    userName: Annotated[str, Query(max_length=10)] = ...
    userEmail: Annotated[str, Query(pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$")] = ...
    userStatement: Annotated[str, Query(min_length=15, max_length=200)] = ...
    requestedDate: str = ...


class LanguageResDto(BaseModel):
    userId: str
    userName: str
    userEmail: str
    userStatement: str
    requestedDate: str
