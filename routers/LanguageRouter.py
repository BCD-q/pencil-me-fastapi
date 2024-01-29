from fastapi import APIRouter, Body, Depends
from typing import Annotated
from dto.LanguageDto import LanguageReqDto
from dto.CommonDto import CommonResDto
from service.LanguageService import get_language_service, LanguageService

router = APIRouter(
    prefix="/language",
    tags=["language"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", status_code=200, response_model=CommonResDto)
async def request_to_language_model(language_req_dto: Annotated[LanguageReqDto, Body(
        example=
        {
            "userId": "1",
            "userName": "홍길동",
            "userEmail": "test@test.com",
            "userStatement": "내일 저녁 6시에 친구랑 잠실종합운동장역 앞에서 만나기로 했어. 친구랑 만난 후에는 조용필 콘서트를 볼거야",
            "requestedDate": "2021-11-22T14"
        })
    ],
        language_service: LanguageService = Depends(get_language_service)):
    return language_service.request_ai_response(language_req_dto)
