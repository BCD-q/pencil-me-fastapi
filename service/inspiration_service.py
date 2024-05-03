from service.component.google_search_engine import GoogleSearchEngineService
from service.component.page_crawler import PageCrawler
from service.component.langchain import LangChain
from service.component.request_to_spring_server import RequestToSpringServer
from dto.inspiration import SuggestionForMeResDto, SuggestionOfTheDayDto, SuggestionForMeReqDto
from dto.langchain import LangChainSummarizeWebBodyResponse
from dto.language import LanguageReqDto, MemberInfoReqDto


class InspirationService:
    def __init__(self, google_search_engine: GoogleSearchEngineService, page_crawler: PageCrawler,
                 langchain: LangChain, request_to_spring_server: RequestToSpringServer):
        self.google_search_engine = google_search_engine
        self.page_crawler = page_crawler
        self.langchain = langchain
        self.request_to_spring_server = request_to_spring_server

    def suggestion_for_me(self, suggestion_for_me_req_dto: SuggestionForMeReqDto, start: int) -> list[SuggestionForMeResDto]:
        result = self.google_search_engine.suggestion_for_me(suggestion_for_me_req_dto.keyword, start)
        suggestion_for_me_res_list = []
        for i in result['items']:
            # pagemap의 cse_thumnail이 없을 경우 빈 값으로 대체
            try:
                thumbnail_url = i['pagemap']['cse_thumbnail'][0]['src']
            except KeyError:
                thumbnail_url = ""
            suggestion_for_me_res_list.append(SuggestionForMeResDto(
                title=i['title'],
                link=i['link'],
                thumbnail_url=thumbnail_url
            ))
        return suggestion_for_me_res_list

    def add_it_right_away(self, member_info_req_dto: MemberInfoReqDto, url: str):
        page_summary = self.page_summary(url)
        keyword = self.langchain.determine_keyword(page_summary['title'])
        saved_keyword_id = self.request_to_spring_server.save_category(keyword)
        return self.langchain.summarize_web_body_and_dialog(page_summary, member_info_req_dto, saved_keyword_id)

    def page_summary(self, url: str) -> LangChainSummarizeWebBodyResponse:
        # page_crawler에서 페이지 크롤링 메소드 호출
        body_text = self.page_crawler.get_page_contents(url)
        return self.langchain.summarize_web_page_body(body_text)
