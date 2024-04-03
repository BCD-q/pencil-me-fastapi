from dependency_injector import containers, providers

from service.google_search_engine import GoogleSearchEngineService
from service.langchain_service import LangChainService
from service.inspiration_service import InspirationService
from service.llm_service import LLMService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["routers.language_router", "routers.inspiration_router"])
    config = providers.Configuration()

    # LangchainService의 인스턴스를 싱글톤으로 관리
    langchain_service = providers.Singleton(LangChainService)
    # Google Search Engine을 싱글톤으로 관리
    google_search_engine = providers.Singleton(GoogleSearchEngineService)

    # LLMService에 langchain_service 프로바이더의 인스턴스를 주입
    llm_service = providers.Factory(
        LLMService,
        langchain_service=langchain_service
    )

    # InspirationService에 인스턴스 주입
    inspiration_service = providers.Factory(
        InspirationService,
        google_search_engine_service=google_search_engine
    )

