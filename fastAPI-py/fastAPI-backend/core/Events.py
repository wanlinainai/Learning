from typing import Callable

from aioredis import Redis
from fastapi import FastAPI

from database.cache_redis import sys_cache, code_cache
from database.db_mysql import register_mysql


# 启动事件
def startup(app: FastAPI) -> Callable:
    async def app_start() -> None:
        print("项目启动")
        # 注册数据库
        await register_mysql(app)

        # 注入缓存到app state
        app.state.cache = await sys_cache()
        app.state.code_cache = await code_cache()

        pass
    return app_start

# 停止事件
def stopping(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        print("程序关闭!")
        cache: Redis = await app.state.cache
        code: Redis = await app.state.code_cache
        await cache.close()
        await code.close()
    return stop_app