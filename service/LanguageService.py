from dto.LanguageDto import LanguageReqDto, LanguageResDto, LanguageResDtoDescription
from datetime import datetime
import os
import openai
from dotenv import load_dotenv
from dto.CommonDto import CommonResDto
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

AI_MODEL = "gpt-3.5-turbo-1106"
INSUFFICIENT_MONEY_MSG = "계정 요금이 충분하지 않습니다."
API_ERROR_MSG = "API 요청에 문제가 있습니다. 관리자에게 문의하세요"
IO_ERROR_MSG = "I/O에 문제가 있습니다. 관리자에게 문의하세요"

language_res_dto = LanguageResDtoDescription(
    userId="Include who_requested_uid in the userId",
    groupId="Include group_id in groupId",
    title="In the title, include a one- or two-line summary sentence that summarizes the user's answer. "
          "For example, if the user answered, "
          """I need to finish my computer algorithms assignment by 12:00 tomorrow night,
          "" you could say, ""Finish my computer algorithms assignment.""",
    contents="contents doesn't need to be populated with anything.",
    deadline='Inside the deadline, you can infer the deadline as a date and time based on the date in today''s date. '
             'For example, "I have an assignment due tomorrow", the date would be today''s date plus one day.'
             'If the user said words like "lunch," "dinner," or "morning" without giving a specific time, '
             'you can include a representative time for each word. For example, '
             'lunch would be 12:00 pm and dinner would be 6:00 pm. '
             'Responses to all deadlines should be in the format YYYY-MM-DDThh-mm.'
             'If a user''s response contains no information, please mark it as null'
)

serialized_class = language_res_dto.model_dump_json()


def create_todo_prompt(self, who_requested_name, who_requested_uid, group_id):
    # 요청 메소드 기준 위치로 설정해야 됨
    prompt1 = open('resource/request_prompt_less_token.txt', 'r', encoding='utf-8')
    response = (f"{prompt1.read()} \nwho_requested_name: {who_requested_name},  who_requested_uid: {who_requested_uid},"
                f"today's date: {datetime.now()}, group_id: {group_id},"
                f"Response Model Description: {serialized_class}")
    prompt1.close()
    print(response)
    return response


def create_group_keyword(self):
    response = ('Pick a keyword from a user''s post.'
                'For example, "I''m going to go to an amusement park" would be "play." '
                'Another example: "I''m going to study" would be "study" or "self-development"'
                '<rule> Answer with words in Korean  </rule> When selecting keywords, '
                'try to choose words that are representative of similar words and use them in your'
                'When choosing keywords, try to choose words that are representative of similar words, '
                'for example, "barbecue" and "hamburger" can be "food", and '
                '"performance" and "amusement park" can be "activity". <rule> One word answer. </rule>')
    return response


class LanguageService:

    def request_ai_response(self, language_req_dto: LanguageReqDto) -> CommonResDto:
        try:
            openai_group_title_result = openai.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system",
                     "content": create_group_keyword(self)},
                    {"role": "user",
                     "content": language_req_dto.userStatement}
                ]
            )
            # 서버로 요청을 보낼 키워드
            group_keyword = openai_group_title_result.choices[0].message.content
            print(group_keyword)
            # 서버로부터 응답 받은 값
            given_group_id = 1

            openai_result = openai.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system",
                     "content": create_todo_prompt(self, language_req_dto.userName, language_req_dto.userId, given_group_id)},
                    {"role": "user",
                     "content": language_req_dto.userStatement}
                ]
            )
            response = CommonResDto(
                msg="결과가 정상적으로 불러와졌습니다.",
                result=json.loads(openai_result.choices[0].message.content)
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
