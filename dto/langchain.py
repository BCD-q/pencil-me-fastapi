from langchain_core.pydantic_v1 import BaseModel, Field
from datetime import datetime


class LangChainSummarizeDialogResponse(BaseModel):
    memberId: int = Field(description="""<important!>Include in prefix 'member_id' in the memberId</important!>""")
    categoryId: int = Field(description="Include in prefix 'category_id' in categoryId")
    title: str = Field(description="""
    In the title, include a one- or two-line summary sentence that summarizes the user's answer. "
          "For example, if the user answered, "
          I need to finish my computer algorithms assignment by 12:00 tomorrow night,
          "" you could say, ""Finish my computer algorithms assignment.
                                      """)
    contents: str = Field(description="Take notes summarizing the user's sentence. If there is no content, output null "
                                      "<important!>None is null</important!> ")
    deadline: datetime = Field(description="""
                                            Inside the deadline, you can infer the deadline as a date and time "
                                           <important>"based on the date in '!prefix_requestedDate!'.</important> 
                                           Inside the deadline, you can infer the deadline as a date and time based on the date in today''s date. '
                                            'For example, "I have an assignment due tomorrow", the date would be today''s date plus one day.'
                                            'If the user said words like "lunch," "dinner," or "morning" without giving a specific time, '
                                             'you can include a representative time for each word. For example, '
                                            'lunch would be 12:00 pm and dinner would be 6:00 pm. '
                                                                                """)


class LangChainSummarizeWebBodyResponse(BaseModel):
    title: str = Field(description="This should contain the title of the summarized sentence.")
    contents: str = Field(description="This should contain 2-3 lines of summarized text. and Skip the line if it gets "
                                      "too long")


class LangChainSummarizeLangChainSummarizeWebBodyResponse(BaseModel):
    memberId: int = Field(description="""<important!>Include in prefix 'member_id' in the memberId</important!>""")
    categoryId: int = Field(description="Include in prefix 'category_id' in categoryId")
    title: str = Field(description="""
                                    In the title, include a one- or two-line summary sentence that summarizes the user's answer. "
                                          """)
    contents: str = Field(description="Take notes summarizing the user's sentence. If there is no content, output null "
                                      "<important!>None is null</important!> ")

class LangChainSuggestTaskResponse(BaseModel):
    tasks: list[str] = Field(description="Include in prefix 'tasks' in the tasks")