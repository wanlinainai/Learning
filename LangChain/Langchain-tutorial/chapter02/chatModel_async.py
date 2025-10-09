import asyncio
import os
import dotenv
import time

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

chat_model = ChatOpenAI(
    model="gpt-4o-mini"
)

# 同步
def sync_test():
    messages = [SystemMessage(content="你是一个智能助手"), HumanMessage(content="简要概述一下1+1=？")]
    start_time = time.time()
    response = chat_model.invoke(messages)
    duration = time.time() - start_time
    print(f"同步耗时长: {duration}")
    return response, duration

# 异步
async def async_test():
    messages = [SystemMessage(content="你是一个智能助手小废"), HumanMessage(content="你是谁")]
    start_time = time.time()
    response = await chat_model.ainvoke(messages)
    duration = time.time() - start_time
    print(f"异步耗时: {duration}")
    return response, duration

if __name__ == '__main__':
    sync_response, syncDuration = sync_test()
    print(f"同步响应内容: {sync_response.content}")

    async_response, asyncDuration = asyncio.run(async_test())
    print(f"异步响应内容：{async_response.content}")

    # 并发测试
    print("==========并发测试===========")
    start_time = time.time()
    async def run_concurrent_tests():
        tasks = [async_test() for _ in range(10)]
        return await asyncio.gather(*tasks)

    results = asyncio.run(run_concurrent_tests())

    total_time = time.time() - start_time
    print(f"\n3个并发总耗时: {total_time:.2f}S")
    print(f"\n平均耗时：{total_time / 3:.2f}S")
