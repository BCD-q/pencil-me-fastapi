from langchain_core.pydantic_v1 import BaseModel, Field
from datetime import datetime


class LangChainResponse(BaseModel):
    memberId: int = Field(description="""Include in prefix 'member_id' in the memberId""")
    categoryId: int = Field(description="Include in prefix 'category_id' in categoryId")
    title: str = Field(description="""In the title, include a one- or two-line summary sentence 
                                      that summarizes in the suffix 'user_dialog'""")
    contents: str = Field(description="Take notes summarizing the user's sentence. If there is no content, output null "
                                      "<important!>None is null</important> ")
    deadline: datetime = Field(description="Inside the deadline, you can infer the deadline as a date and time "
                                           "based on the date in 'current_time'. ")
