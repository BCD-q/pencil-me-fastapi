from fastapi import APIRouter, Body, Depends
from typing import Annotated
from dto.language import LanguageReqDto, LanguageResDto
from dto.common import CommonResDto
from service.language_service import get_language_service, LanguageService
from containers import Container
from dependency_injector.wiring import inject, Provide
from service.llm_service import LLMService

container = Container()
container.wire(modules=[__name__])

router = APIRouter(
    prefix="/language",
    tags=["language"],
    responses={404: {"description": "Not found"}}
)


@router.post("", status_code=201, response_model=CommonResDto)
async def request_to_language_model(language_req_dto: Annotated[LanguageReqDto, Body(
    example=
    {
        "memberId": "1",
        "memberName": "홍길동",
        "memberEmail": "test@test.com",
        "memberStatement": "내일 저녁 6시에 친구랑 잠실종합운동장역 앞에서 만나기로 했어. 친구랑 만난 후에는 조용필 콘서트를 볼거야",
        "requestedDate": "2021-11-22T14:"
    })
],
                                    language_service: LanguageService = Depends(get_language_service)):
    return language_service.request_ai_response(language_req_dto)


@router.post("/test", status_code=201, response_model=LanguageResDto)
@inject
async def test(
        language_req_dto: Annotated[LanguageReqDto, Body(
            example={
                "memberId": "1",
                "memberName": "홍길동",
                "memberEmail": "test@test.com",
                "memberStatement": "내일 저녁 6시에 친구랑 잠실종합운동장역 앞에서 만나기로 했어. 친구랑 만난 후에는 조용필 콘서트를 볼거야",
                "requestedDate": "2021-11-22T14:"
            })
        ],
        llm_service: LLMService = Depends(Provide[Container.llm_service])) -> LanguageResDto:
    return llm_service.request_llm_function(language_req_dto)
