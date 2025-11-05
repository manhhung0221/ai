from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tracers import ConsoleCallbackHandler
from langchain_core.messages import AIMessage
import os 
from dotenv import load_dotenv
load_dotenv(".env")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY",None)
llm=ChatOpenAI(model="gpt-4o-mini",temperature=0.2,api_key=OPENAI_API_KEY)
prompt=ChatPromptTemplate.from_messages([
    ("system","Bạn là một phóng viên giỏi với khả năng tóm tắt các báo kinh tế và đầu tư"),
    ("human","Hãy tóm tắt nội dung bài báo sau không quá 200 từ, nội dung trả về bằng markdown, có các từ khóa quan trọng trong bài báo: {content}")
])
chain=prompt | llm 
response= chain.invoke(
    {'content':'''Cơ hội giảm thuế sâu cho dệt may, thủy sản, nông sản

Ngày 26/10, Việt Nam và Mỹ đã đồng ý công bố Tuyên bố chung về Khuôn khổ Hiệp định Thương mại đối ứng, công bằng và cân bằng. Nhiều thông tin tích cực trong tuyên bố mở ra kỳ vọng mới cho các ngành hàng xuất khẩu chủ lực của Việt Nam.

Trong thời gian tới, hai bên sẽ tiếp tục thảo luận và triển khai các công việc hướng đến việc hoàn tất Hiệp định Thương mại đối ứng, công bằng và cân bằng, trên nguyên tắc cởi mở, xây dựng, bình đẳng, tôn trọng độc lập, tự chủ, thể chế chính trị, cùng có lợi và cân nhắc đến trình độ phát triển của mỗi bên.

Ngành xuất khẩu nào sẽ được hưởng lợi và có khả năng giảm thuế về 0%?

'''},
    config={"callbacks":[ConsoleCallbackHandler]}
)
if isinstance(response, AIMessage) and response.usage_metadata:
    input_tokens = response.usage_metadata.get("input_tokens")
    output_tokens = response.usage_metadata.get("output_tokens")
    print(f"Input tokens: {input_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(response.usage_metadata)
