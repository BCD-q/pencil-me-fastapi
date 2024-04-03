from fastapi import APIRouter, Body, Depends, Query
from typing import Annotated
from dto.common import CommonResDto
from dto.inspiration import SuggestionForMeReqDto
from containers import Container
from service.inspiration_service import InspirationService
from dependency_injector.wiring import inject, Provide

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

    print(suggestion_for_me_req_dto.keyword)
    inspiration_service.google_search_engine_service.google_search_engine(suggestion_for_me_req_dto.keyword)
    return CommonResDto(
        msg="The inspiration",
        result={
            "hi": suggestion_for_me_req_dto.keyword
        }
    )
