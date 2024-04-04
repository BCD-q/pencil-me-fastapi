from dependency_injector import containers, providers

from service.component.google_search_engine import GoogleSearchEngineService
from service.component.langchain import LangChain
from service.inspiration_service import InspirationService
from service.llm_service import LLMService
from service.component.page_crawler import PageCrawler
from service.component.request_to_spring_server import RequestToSpringServer


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["routers.language_router", "routers.inspiration_router"])
    config = providers.Configuration()

    # LangchainService의 인스턴스를 싱글톤으로 관리
    langchain = providers.Singleton(LangChain)
    # Google Search Engine을 싱글톤으로 관리
    google_search_engine = providers.Singleton(GoogleSearchEngineService)
    # Page Crawler
    page_crawler = providers.Singleton(PageCrawler)
    # Request To Spring Server
    request_to_spring_server = providers.Singleton(RequestToSpringServer)

    # LLMService에 langchain_service 프로바이더의 인스턴스를 주입
    llm_service = providers.Factory(
        LLMService,
        langchain=langchain,
        request_to_spring_server=request_to_spring_server
    )

    # InspirationService에 인스턴스 주입
    inspiration_service = providers.Factory(
        InspirationService,
        google_search_engine=google_search_engine,
        page_crawler=page_crawler,
        langchain=langchain
    )

