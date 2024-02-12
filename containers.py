from dependency_injector import containers, providers
from service.langchain_service import LangChainService
from service.llm_service import LLMService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["routers.language_router"])
    config = providers.Configuration()

    # LangchainService의 인스턴스를 싱글톤으로 관리
    langchain_service = providers.Singleton(LangChainService)

    # LLMService에 langchain_service 프로바이더의 인스턴스를 주입
    llm_service = providers.Factory(
        LLMService,
        langchain_service=langchain_service
    )
