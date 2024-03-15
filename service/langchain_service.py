from datetime import datetime

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from dto.language import LanguageResDto, LanguageReqDto
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 입력과 예시의 유사도에 따라 몇가지의 예제를 선택해주는 선택기
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
# 예시들의 위치를 저장할 벡터 저장소
from langchain_community.vectorstores import Chroma
# 문자들을 벡터로 변환해주는 임베딩 클래스
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
import json
from pathlib import Path

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)


class LangChainResponse(BaseModel):
    memberId: int = Field(description="""Include in prefix 'member_id' in the memberId""")
    categoryId: int = Field(description="Include in prefix 'category_id' in categoryId")
    title: str = Field(description="""In the title, include a one- or two-line summary sentence 
                                      that summarizes in the suffix 'user_dialog'""")
    contents: str = Field(description="Take notes summarizing the user's sentence. If there is no content, output null "
                                      "<important!>None is null</important> ")
    deadline: datetime = Field(description="Inside the deadline, you can infer the deadline as a date and time "
                                           "based on the date in 'current_time'. ")


class LangChainService:
    def __init__(self):
        pass

    @staticmethod
    def determine_keyword(user_dialog: str) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            Pick a keyword from a user's post. For example, "I'm going to go to an amusement park" would be "play." 
            Another example: "I'm going to study" would be "study" or "self-development". <rule> Answer with 
            words in Korean  </rule> When selecting keywords, try to choose words that are representative of similar 
            words and use them in your When choosing keywords, try to choose words that are representative of similar 
            words, for example, "barbecue" and "hamburger" can be "food", and 
            "performance" and "amusement park" can be "activity". <rule> One word answer. 
            let me show some example</rule>
            <example>
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
            </example>
            """),
            ("user", "{input}")
        ])

        output_parser = StrOutputParser()

        chain = prompt | model | output_parser

        return chain.invoke({
            "input": user_dialog
        })

    @staticmethod
    def summarize_dialog(language_req_dto: LanguageReqDto, saved_keyword_id):
        # 컨테이너 기준으로 경로를 설정해줘야 함
        file_path = 'resource/corrected_detailed_events.json'
        example = json.loads(Path(file_path).read_text(encoding='UTF8'))

        parser = JsonOutputParser(pydantic_object=LangChainResponse)

        example_prompt = PromptTemplate(
            template="{user_dialog}\n{answer}",
            input_variables=["user_dialog", "answer"]
        )

        example_selector = SemanticSimilarityExampleSelector.from_examples(
            example,
            OpenAIEmbeddings(),
            Chroma,
            k=4
        )

        prompt = FewShotPromptTemplate(
            example_selector=example_selector,
            example_prompt=example_prompt,
            suffix="user_dialog: {user_dialog}",
            prefix="{format_instructions}, {current_time}, {member_id}, {category_id}",
            input_variables=["user_dialog"],
            partial_variables={"format_instructions": parser.get_format_instructions(),
                               "member_id": language_req_dto.memberId,
                               "category_id": saved_keyword_id,
                               "current_time": str(datetime.now())}
        )

        chain = prompt | model | parser

        result = chain.invoke({
            "user_dialog": "user_dialog: " + language_req_dto.memberStatement
        })

        return LanguageResDto(
            memberId=result['memberId'],
            categoryId=result['categoryId'],
            title=result['title'],
            contents=result['contents'],
            deadline=result['deadline']
        )
