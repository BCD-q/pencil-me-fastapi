from service.component.google_search_engine import GoogleSearchEngineService
from service.component.page_crawler import PageCrawler
from service.component.langchain import LangChain
from dto.inspiration import SuggestionForMeResDto, SuggestionOfTheDayDto
from dto.langchain import LangChainSummarizeWebBodyResponse
from dto.language import LanguageReqDto


class InspirationService:
    def __init__(self, google_search_engine: GoogleSearchEngineService, page_crawler: PageCrawler, langchain: LangChain):
        self.google_search_engine = google_search_engine
        self.page_crawler = page_crawler
        self.langchain = langchain

    def suggestion_of_the_day(self) -> list[SuggestionOfTheDayDto]:
        result = self.google_search_engine.suggestion_of_the_day()
        suggestions_of_the_day_list = []
        for i in result['items']:
            # pagemap의 cse_thumnail이 없을 경우 빈 값으로 대체
            try:
                thumbnail_url = i['pagemap']['cse_thumbnail'][0]['src']
            except KeyError:
                thumbnail_url = ""
            suggestions_of_the_day_list.append(SuggestionOfTheDayDto(
                title=i['title'],
                link=i['link'],
                thumbnail_url=thumbnail_url
            ))
        return suggestions_of_the_day_list

    def suggestion_for_me(self, search_keyword: list[str]) -> list[SuggestionForMeResDto]:
        result = self.google_search_engine.suggestion_for_me(search_keyword)
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
            print(i)

        return suggestion_for_me_res_list

    # 페이지 요약 후 할일로 변환
    # 사용자 정보와 URL을 받아서 작업을 수행한다.
    def add_it_right_away(self, language_req_dto: LanguageReqDto, url: str):
        # 하단 page_summary 호출 후 페이지 요약 정보를 저장한다.
        page_summary = self.page_summary(url)
        # page_summary를 함수로 보내 키워드 추출
        
        # langchain에서 할 일 등록 메소드 호출
        self.langchain.summarize_web_body_and_dialog(page_summary)
        return

    def page_summary(self, url: str) -> LangChainSummarizeWebBodyResponse:
        # page_crawler에서 페이지 크롤링 메소드 호출
        body_text = self.page_crawler.get_page_contents(url)
        return self.langchain.summarize_web_page_body(body_text)
