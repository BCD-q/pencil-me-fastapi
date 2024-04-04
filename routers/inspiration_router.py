from fastapi import APIRouter, Body, Depends, Query
from typing import Annotated
from dto.common import CommonResDto
from dto.inspiration import SuggestionForMeReqDto
from containers import Container
from service.inspiration_service import InspirationService
from dependency_injector.wiring import inject, Provide
from dto.language import LanguageReqDto

router = APIRouter(
    prefix="/inspiration",
    tags=["inspiration"],
    responses={404: {"description": "Not found"}}
)

container = Container()
container.wire(modules=[__name__])


@router.get("/day", status_code=200, response_model=CommonResDto)
def suggestion_of_the_day():
    return CommonResDto(
        msg="The inspiration",
        result={
            "hi": "Hello World!"
        }
    )


@router.post("/me", status_code=200, response_model=CommonResDto)
@inject
def suggestion_for_me(suggestion_for_me_req_dto: Annotated[SuggestionForMeReqDto, Body(
    example={
        "keyword": ["키워드1", "키워드2", "키워드3"]
    })
], inspiration_service: InspirationService = Depends(Provide[Container.inspiration_service])):
    return CommonResDto(
        msg="The inspiration",
        result={
            "data": inspiration_service.suggestion_for_me(suggestion_for_me_req_dto.keyword)
        }
    )


@router.get("/page-crawler", status_code=200, response_model=CommonResDto)
@inject
def page_crawler(url: str, inspiration_service: InspirationService = Depends(Provide[Container.inspiration_service])):
    return CommonResDto(
        msg="The inspiration",
        result={
            "data": inspiration_service.page_summary(url)
        }
    )

@router.post("/todo/new", status_code=201, response_model=CommonResDto)
@inject
def add_it_right_away_todo(
    url: str,
        # 사용자 정보가 담긴 DTO 객체를 만들어야 함 (수정)
    language_req_dto: Annotated[LanguageReqDto, Body(
            example={
                "memberId": 1,
                "memberName": "홍길동",
                "memberEmail": "test@test.com",
                "memberStatement": "내일 저녁 6시에 친구랑 잠실종합운동장역 앞에서 만나기로 했어. 친구랑 만난 후에는 조용필 콘서트를 볼거야",
                "requestedDate": "2021-11-22T14:00"
            })
        ],
        inspiration_service: InspirationService = Depends(Provide[Container.inspiration_service])):
    return CommonResDto(
        msg="The inspiration",
        result={
            # 사용자 정보와 URL을 파라미터로 넘긴다.
            "data": inspiration_service.add_it_right_away(language_req_dto, url)
        }
    )