from fastapi import APIRouter, Query, Body
from typing import Annotated
from pydantic import BaseModel
from dto.Language import LanguageReqDto, LanguageResDto
from service.LanguageService import LanguageService

router = APIRouter(
    prefix="/language",
    tags=["language"],
    responses={404: {"description": "Not found"}}
)
language_service = LanguageService()

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
    return await language_service.test_method(language_req_dto)
