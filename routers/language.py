from fastapi import APIRouter, Query, Body
from typing import Annotated
from pydantic import BaseModel

router = APIRouter(
    prefix="/language",
    tags=["language"],
    responses={404: {"description": "Not found"}}
)


class UserInformation(BaseModel):
    userId: str = ...
    userName: Annotated[str, Query(max_length=10)] = ...
    userEmail: Annotated[str, Query(pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$")] = ...


class LanguageReqDto(BaseModel):
    userInformation: UserInformation
    userStatement: Annotated[str, Query(min_length=15, max_length=200)] = ...
    requestedDate: str = ...


@router.post("/", status_code=200)
async def request_to_language_model(language_req_dto: Annotated[
    LanguageReqDto,
    Body(
        example=
        {
            "userInformation": {
                "userId": "1",
                "userName": "홍길동",
                "userEmail": "test@test.com"
            },
            "userStatement": "내일 저녁 6시에 친구랑 잠실종합운동장역 앞에서 만나기로 했어. 친구랑 만난 후에는 조용필 콘서트를 볼거야",
            "requestedDate": "2021-11-22T14:"
        }

    )
]):
    return language_req_dto
