
from service.component.langchain import LangChain
from service.component.request_to_spring_server import RequestToSpringServer
from dto.language import LanguageResDto, LanguageReqDto



class LLMService:
    def __init__(self, langchain: LangChain, request_to_spring_server: RequestToSpringServer):
        self.langchain = langchain
        self.request_to_spring_server = request_to_spring_server

    # languageReq -> languageRes
    def request_llm_function(self, language_req_dto: LanguageReqDto, authorization: str) -> LanguageResDto:
        # languageReq -> userDialog를 함수로 보내 키워드 추출
        keyword = self.langchain.determine_keyword(language_req_dto.memberStatement)
        # 키워드: str을 스프링 서버로 저장 요청 보냄; 저장된 id를 리턴 받음
        saved_keyword_id = self.request_to_spring_server.save_category(keyword, authorization)
        # 반환된 id함께 languageReq를 함수로 보내 LanguageRes를 반환받음
        # 결과로 반환받은 LanguageRes를 반환
        return self.langchain.summarize_dialog(language_req_dto, saved_keyword_id)
