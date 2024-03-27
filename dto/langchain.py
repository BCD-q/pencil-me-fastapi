from langchain_core.pydantic_v1 import BaseModel, Field
from datetime import datetime


class LangChainResponse(BaseModel):
    memberId: int = Field(description="""Include in prefix 'member_id' in the memberId""")
    categoryId: int = Field(description="Include in prefix 'category_id' in categoryId")
    title: str = Field(description="""In the title, include a one- or two-line summary sentence 
                                      that summarizes in the 'user_dialog' <important!>it must be summarized and Must be related to user_dialog.</important!>
                                      <example>"내일 저녁에 친구랑 만나서 놀기로 했어" is "친구와의 만남"</example>
                                      """)
    contents: str = Field(description="Take notes summarizing the user's sentence. If there is no content, output null "
                                      "<important!>None is null</important> ")
    deadline: datetime = Field(description="Inside the deadline, you can infer the deadline as a date and time "
                                           "based on the date in 'current_time'. ")
