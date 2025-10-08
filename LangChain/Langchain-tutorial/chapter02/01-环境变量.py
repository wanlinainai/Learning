from langchain_openai import ChatOpenAI
import os

chat_model = ChatOpenAI(
    model="gpt-4o-mini",
    base_url=os.environ["OPENAI_BASE_URL"],
    api_key=os.environ["OPENAI_API_KEY"]
)

response = chat_model.invoke("你好")
print(response.content)