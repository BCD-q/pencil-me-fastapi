from service.component.google_search_engine import GoogleSearchEngineService
from service.component.page_crawler import PageCrawler
from service.component.langchain import LangChain
from dto.inspiration import SuggestionForMeResDto, SuggestionOfTheDayDto


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

    def add_it_right_away(self):
        # 페이지 요약 후 할일로 변환
        # 하단 page_summary 호출 후
        # langchain에서 할 일 등록 메소드 호출
        pass

    def page_summary(self, url: str):
        # page_crawler에서 페이지 크롤링 메소드 호출
        body_text = self.page_crawler.get_page_contents(url)
        self.langchain.summarize_body(body_text)
        pass
