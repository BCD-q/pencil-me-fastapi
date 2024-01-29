from dto.Language import LanguageReqDto
from datetime import datetime
import os
import openai
from dotenv import load_dotenv
from dto.Common import CommonResDto
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

AI_MODEL = "gpt-3.5-turbo-1106"
INSUFFICIENT_MONEY_MSG = "계정 요금이 충분하지 않습니다."
API_ERROR_MSG = "API 요청에 문제가 있습니다. 관리자에게 문의하세요"
IO_ERROR_MSG = "I/O에 문제가 있습니다. 관리자에게 문의하세요"


def openai_dynamic_prompt(self, who_requested_name, who_requested_uid):
    # 요청 메소드 기준 위치로 설정해야 됨
    prompt1 = open('resource/request_prompt_less_token.txt', 'r', encoding='utf-8')
    response = f"{prompt1.read()} \n요청자: {who_requested_name}  요청자 ID: {who_requested_uid}  오늘 날짜: {datetime.now()}, "
    prompt1.close()
    return response


class LanguageService:

    def test_method(self, language_req_dto: LanguageReqDto) -> CommonResDto:
        # LanguageReqDto 객체에서 필드 값들을 추출하여 LanguageResDto 객체를 생성하여 반환합니다.
        try:
            openai_result = openai.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system",
                     # 차후에 USER이름과 유저 id를 포함시켜야 함
                     "content": openai_dynamic_prompt(self, "name", 1234)},
                    {"role": "user",
                     "content": language_req_dto.userStatement}
                ]
            )
            response = CommonResDto(
                msg= "결과가 정상적으로 불러와졌습니다.",
                result= json.loads(openai_result.choices[0].message.content)
            )
        except openai.RateLimitError:
            response = CommonResDto(msg=INSUFFICIENT_MONEY_MSG)
        except openai.APIError:
            response = CommonResDto(msg=API_ERROR_MSG)
        except FileNotFoundError:
            response = CommonResDto(msg=IO_ERROR_MSG)
        return response


def get_language_service() -> LanguageService:
    return LanguageService()
