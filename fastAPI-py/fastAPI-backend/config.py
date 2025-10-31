import os.path
from typing import List

from pydantic import BaseSettings


class Config(BaseSettings):
    # 调试模式
    APP_DEBUG: bool = True
    # 项目信息
    VERSION: str = "0.0.1"
    PROJECT_NAME: str = "fastapi-demo"
    DESCRIPTION: str = "fastapi项目DEMO"
    # 静态资源目录
    STATIC_DIR: str = os.path.join(os.getcwd(), "static")
    # Session密钥
    SECRET_KEY: str = "your-secret-key-here-change-in-production"

    # 跨域请求
    CORS_ORIGINS: List[str] = ['*']
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ['*']
    CORS_ALLOW_HEADERS: List[str] = ['*']

settings = Config()