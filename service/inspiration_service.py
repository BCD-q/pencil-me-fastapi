from service.google_search_engine import GoogleSearchEngineService
class InspirationService:
    def __init__(self, google_search_engine_service: GoogleSearchEngineService):
        self.google_search_engine_service = google_search_engine_service

    def request_search(self, search_keyword: list[str]):
        self.google_search_engine_service.google_search_engine(search_keyword)