from service.langchain_service import LangChainService


class LLMService:
    def __init__(self, langchain_service: LangChainService):
        self.langchain_service = langchain_service

    def call_function(self):
        self.langchain_service.get_response()
