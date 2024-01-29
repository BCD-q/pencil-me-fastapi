from test.Language import LanguageResDto, LanguageReqDto


class TestService:
    def test_method(self, language_req_dto: LanguageReqDto) -> LanguageResDto:
        # LanguageReqDto 객체에서 필드 값들을 추출하여 LanguageResDto 객체를 생성하여 반환합니다.
        return LanguageResDto(
            userId=language_req_dto.userId,
            userName=language_req_dto.userName,
            userEmail=language_req_dto.userEmail,
            userStatement=language_req_dto.userStatement,
            requestedDate=language_req_dto.requestedDate
        )


def get_test_service() -> TestService:
    return TestService()


