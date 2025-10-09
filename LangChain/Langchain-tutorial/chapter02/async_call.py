import asyncio
import time

async def async_call(llm):
    await asyncio.sleep(3)
    print("异步调用End")

async def perform_other_tasks():
    await asyncio.sleep(3)
    print("其他任务完成...")

async def run_async_tasks():
    start_time = time.time()
    await asyncio.gather(
        async_call(None),
        perform_other_tasks()
    )
    end_time = time.time()
    return f"共耗时:{end_time - start_time}"

if __name__ == '__main__':
    result = asyncio.run(run_async_tasks())
    print(result)