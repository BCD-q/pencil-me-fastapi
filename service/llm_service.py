import os

from requests import RequestException

from service.langchain_service import LangChainService
from dto.language import LanguageResDto, LanguageReqDto
import requests

URL = os.getenv('SPRING_SERVER_URL')


class LLMService:
    def __init__(self, langchain_service: LangChainService):
        self.langchain_service = langchain_service

    # languageReq -> languageRes
    def request_llm_function(self, language_req_dto: LanguageReqDto) -> LanguageResDto:
        print(language_req_dto)
        # languageReq -> userDialog를 함수로 보내 키워드 추출
        keyword = self.langchain_service.determine_keyword(language_req_dto.memberStatement)
        # 키워드: str을 스프링 서버로 저장 요청 보냄; 저장된 id를 리턴 받음
        print(keyword)
        try:
            server_response = requests.post(URL, json={"name": keyword})
            saved_keyword_id = server_response.json()['data']['categoryId']
        except RequestException:
            saved_keyword_id = 1
        # 반환된 id함께 languageReq를 함수로 보내 LanguageRes를 반환받음
        # 결과로 반환받은 LanguageRes를 반환
        return self.langchain_service.summarize_dialog(language_req_dto, saved_keyword_id)
