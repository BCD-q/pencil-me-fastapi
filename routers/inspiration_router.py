from fastapi import APIRouter, Body, Depends, Header
from typing import Annotated, Union
from dto.common import CommonResDto
from dto.inspiration import SuggestionForMeReqDto
from containers import Container
from service.inspiration_service import InspirationService
from dependency_injector.wiring import inject, Provide
from dto.language import LanguageReqDto, MemberInfoReqDto

router = APIRouter(
    prefix="/inspiration",
    tags=["inspiration"],
    responses={404: {"description": "Not found"}}
)

container = Container()
container.wire(modules=[__name__])


@router.post("/me", status_code=200, response_model=CommonResDto)
@inject
def suggestion_for_me(suggestion_for_me_req_dto: Annotated[SuggestionForMeReqDto, Body(
    example={
        "keyword": ["키워드1", "키워드2", "키워드3"]
    })
], start: int, inspiration_service: InspirationService = Depends(Provide[Container.inspiration_service])):
    return CommonResDto(
        msg="영감 데이터 조회 완료 page:" + str(start),
        result={
            "data": inspiration_service.suggestion_for_me(suggestion_for_me_req_dto, start)
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
        language_req_dto: Annotated[MemberInfoReqDto, Body(
            example={
                "memberId": 1,
                "memberName": "홍길동",
                "memberEmail": "test@test.com"
            })
        ],
        token: Union[str, None] = Header(default=None),
        inspiration_service: InspirationService = Depends(Provide[Container.inspiration_service])):
    return CommonResDto(
        msg="제공된 링크로부터 할 일이 생성되었습니다.",
        result={
            # 사용자 정보와 URL을 파라미터로 넘긴다.
            "data": inspiration_service.add_it_right_away(language_req_dto, url, token)
        }
    )
