from fastapi import APIRouter, Query, Body
from typing import Annotated
from pydantic import BaseModel
from dto.Language import LanguageReqDto, LanguageResDto
router = APIRouter(
    prefix="/language",
    tags=["language"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", status_code=200, response_model=LanguageResDto)
async def request_to_language_model(language_req_dto: Annotated[
    LanguageReqDto,
    Body(
        example=
        {
            "userId": "1",
            "userName": "홍길동",
            "userEmail": "test@test.com",
            "userStatement": "내일 저녁 6시에 친구랑 잠실종합운동장역 앞에서 만나기로 했어. 친구랑 만난 후에는 조용필 콘서트를 볼거야",
            "requestedDate": "2021-11-22T14:"
        }

    )
]):
    print(language_req_dto.userId)
    dto_instance = LanguageResDto(
        userId=language_req_dto.userId,
        userName=language_req_dto.userName,
        userEmail=language_req_dto.userEmail,
        userStatement=language_req_dto.userStatement,
        requestedDate=language_req_dto.requestedDate
    )
    return dto_instance
