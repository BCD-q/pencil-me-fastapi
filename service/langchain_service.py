from datetime import datetime

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from dto.language import LanguageResDto, LanguageReqDto

# 입력과 예시의 유사도에 따라 몇가지의 예제를 선택해주는 선택기
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
# 예시들의 위치를 저장할 벡터 저장소
from langchain_community.vectorstores import Chroma
# 문자들을 벡터로 변환해주는 임베딩 클래스
from langchain_openai import OpenAIEmbeddings

import json
from pathlib import Path

model = ChatOpenAI(temperature=0)

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
    def get_response(language_req_dto: LanguageReqDto, saved_keyword_id):
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
            k=1
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