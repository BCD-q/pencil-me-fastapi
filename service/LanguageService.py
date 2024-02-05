from dto.Language import LanguageReqDto, LanguageResDto, LanguageResDtoDescription
from datetime import datetime
import os
import openai
from dotenv import load_dotenv
from dto.Common import CommonResDto
import json
import requests

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
URL = "https://eb62-175-223-27-96.ngrok-free.app/api/v1/categories"

AI_MODEL = "gpt-3.5-turbo-1106"
INSUFFICIENT_MONEY_MSG = "계정 요금이 충분하지 않습니다."
API_ERROR_MSG = "API 요청에 문제가 있습니다. 관리자에게 문의하세요"
IO_ERROR_MSG = "I/O에 문제가 있습니다. 관리자에게 문의하세요"

language_res_dto = LanguageResDtoDescription(
    memberId="Include who_requested_uid in the memberId",
    categoryId="Include group_id in categoryId",
    title="In the title, include a one- or two-line summary sentence that summarizes the user's answer. "
          "For example, if the user answered, "
          """I need to finish my computer algorithms assignment by 12:00 tomorrow night,
          "" you could say, ""Finish my computer algorithms assignment.""",
    contents="contents doesn't need to be populated with anything.",
    deadline='Inside the deadline, you can infer the deadline as a date and time based on the date in today''s date. '
             'For example, "I have an assignment due tomorrow", the date would be today''s date plus one day.'
             'If the user said words like "lunch," "dinner," or "morning" without giving a specific time, '
             'you can include a representative time for each word. For example, '
             'lunch would be 12:00 pm and dinner would be 6:00 pm. '
             'Responses to all deadlines should be in the format YYYY-MM-DD-hh-mm.'
             'If a user''s response contains no information, please mark it as null'
)

keyword_dict = {
    "운동": "요가, 축구, 조깅, 헬스, 수영, 배드민턴, 등산, 사이클링, 댄스, 크로스핏",
    "음악": "콘서트, 라디오, 악기 연주, 작곡, 노래하기, DJing, 음악 제작, 합창, 재즈 클럽, 비닐 레코드 수집",
    "약속": "네트워킹 이벤트, 동창회, 가족 모임, 친구와의 만찬, 비즈니스 미팅, 온라인 미팅, 커피 미팅, 독서 모임, 봉사 활동, 여행 계획",
    "게임": "비디오 게임, 보드 게임, 카드 게임, 모바일 게임, AR/VR 게임, 온라인 멀티플레이어 게임, 퍼즐 게임, 롤플레잉 게임(RPG), 전략 게임, 스포츠 게임",
    "예술": "그림 그리기, 조각, 사진 촬영, 도자기, 목공예, 디지털 아트, 벽화 그리기, 캘리그래피, 패션 디자인, 인테리어 디자인",
    "여행": "백패킹, 도시 탐험, 해변 휴가, 문화 유산 여행, 등산 여행, 사파리, 크루즈 여행, 음식 여행, 캠핑, 로드 트립",
    "요리": "베이킹, 글루텐 프리 요리, 채식 요리, 퓨전 요리, 와인 시음, 커피 브루잉, 바베큐, 전통 요리, 쿠킹 클래스, 푸드 스타일링",
    "교육": "온라인 코스, 언어 학습, 코딩, 공예 클래스, 금융 교육, 요가 강사 과정, 요리 학교, 예술 학교, 음악 수업, 비즈니스 및 마케팅 세미나",
    "테크놀로지": "프로그래밍, 웹 개발, 앱 개발, 데이터 과학, 인공 지능, 사이버 보안, 게임 개발, 하드웨어 테크, 소프트웨어 해킹, 로봇 공학",
    "건강": " 명상, 스트레스 관리, 아로마테라피, 자연 요법, 건강식 다이어트, 미용 및 스킨케어, 개인 트레이닝, 정신 건강 관리, 타이 마사지, 디톡스 프로그램",
    "자기계발": "목표 설정, 시간 관리, 자기 반성, 생산성 향상, 리더십 개발, 감정 관리, 공개 연설, 창의력 증진, 개인 브랜딩, 습관 형성",
    "문화": "박물관 방문, 역사 도서 읽기, 문화 축제 참여, 고대 유적 탐험, 전통 예술 배우기, 역사적 재연, 세계 문화 체험, 역사 강좌 수강, 문화 유산 보존, 세계 신화 연구",
    "자연": "정원 가꾸기, 야생동물 관찰, 환경 보호 활동, 조류 관찰, 자연보호구역 탐방, 식물학 연구, 지속 가능한 생활, 산림 치유, 해양 보호, 기후 변화 교육",
    "스포츠": "마라톤, 골프, 테니스, 복싱, 스케이트보딩, 서핑, 스노우보딩, 아이스하키, 아치리, 탁구",
    "취미": "종이 접기, 스탬프 수집, 모델 조립, 글쓰기, 수집품, 베이킹, 퀼트 만들기, 보석 공예, 손뜨개, 가죽 공예",
    "여가": "별보기, 독립 영화 감상, 테마 파크 방문, 보트 타기, 낚시, 스파 방문, 와인 투어, 트레져 헌트, 마술 배우기, 에스케이프 룸",
    "패션": "메이크업 아트, 패션 트렌드 분석, DIY 의류 제작, 퍼스널 스타일링, 뷰티 튜토리얼, 네일 아트, 향수 수집, 빈티지 쇼핑, 패션 디자인, 스킨케어 루틴",
    "문학": " 소설 쓰기, 시 낭독, 독서 클럽, 고전 문학 탐색, 전자책 출판, 만화책 수집, 문학 페스티벌, 비평 작성, 독서 마라톤, 창작 워크숍",
    "영화": "단편 영화 제작, 영화 비평, 연극 참여, 영화제 방문, 스크린라이팅, 영화 히스토리 연구, 영화 감독 연구, 즉흥 연기, 뮤지컬 감상, 영화 클럽",
    "커뮤니케이션": "새로운 언어 배우기, 수화 배우기, 토론 클럽, 글로벌 커뮤니케이션, 번역, 문화 교류, 소셜 미디어 전략, 공공 연설, 비언어적 커뮤니케이션, 언어 교환 모임"
}

serialized_keyword_dict = json.dumps(keyword_dict, indent=4, sort_keys=True, ensure_ascii=False)


serialized_class = language_res_dto.model_dump_json()


def create_content_prompt(who_requested_name, who_requested_uid, category_id):
    # 요청 메소드 기준 위치로 설정해야 됨
    prompt = open('resource/request_prompt_less_token.txt', 'r', encoding='utf-8')
    response = (f"{prompt.read()} \nwho_requested_name: {who_requested_name},  who_requested_uid: {who_requested_uid},"
                f"today's date: {datetime.now()}, group_id: {category_id},"
                f"Response Model Description: {serialized_class}")
    prompt.close()
    return response


def create_ai_response(system_content: str, user_content: str):
    try:
        openai_result = openai.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system",
                 # 차후에 USER이름과 유저 id를 포함시켜야 함
                 "content": system_content},
                {"role": "user",
                 "content": user_content}
            ]
        )
        try:
            response = CommonResDto(
                msg="결과가 정상적으로 불러와졌습니다.",
                result=json.loads(openai_result.choices[0].message.content)
            )
        except ValueError:
            return openai_result.choices[0].message.content
    except openai.RateLimitError:
        response = CommonResDto(msg=INSUFFICIENT_MONEY_MSG)
    except openai.APIError:
        response = CommonResDto(msg=API_ERROR_MSG)
    except FileNotFoundError:
        response = CommonResDto(msg=IO_ERROR_MSG)
    return response


class LanguageService:
    def request_ai_response(self, language_req_dto: LanguageReqDto) -> CommonResDto:
        generated_category_name = create_ai_response(
            """
            Pick a keyword from a user's post. For example, "I'm going to go to an amusement park" would be "play." 
            Another example: "I'm going to study" would be "study" or "self-development". <rule> Answer with 
            words in Korean  </rule> When selecting keywords, try to choose words that are representative of similar 
            words and use them in your When choosing keywords, try to choose words that are representative of similar 
            words, for example, "barbecue" and "hamburger" can be "food", and 
            "performance" and "amusement park" can be "activity". <rule> One word answer. 
            let me show some example</rule>
            """ + serialized_keyword_dict,
            language_req_dto.memberStatement
        )
        print(generated_category_name)
        server_response = requests.post(URL, json={"name": generated_category_name})
        if server_response.status_code != 201:
            category_id = 1
        else:
            category_id = server_response.json()['data']['categoryId']

        response = create_ai_response(
            create_content_prompt(language_req_dto.memberName, language_req_dto.memberId, category_id),
            language_req_dto.memberStatement)
        return response


def get_language_service() -> LanguageService:
    return LanguageService()
