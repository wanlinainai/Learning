import asyncio
import sys

def start_main_server():
    import time
    import signal

    pass

if __name__ == '__main__':
    # 运行一个异步事件循环，启动一个主服务器
    if sys.version_info < (3, 10):
        loop = asyncio.get_event_loop()

    else:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()

        asyncio.set_event_loop(loop)

    loop.run_until_complete(start_main_server())