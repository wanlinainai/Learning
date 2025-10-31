from fastapi import FastAPI, HTTPException
from tortoise.exceptions import ValidationError

from config import settings
from core.Events import startup, stopping
from core.Exception import http_exception_handler
from core import Exception

application = FastAPI(
    debug=settings.APP_DEBUG,
    docs_url=None,
    redoc_url=None,
)

# 事件监听
application.add_event_handler("startup", startup(application))
application.add_event_handler("shutdown", stopping(application))

# 异常错误处理
application.add_exception_handler(HTTPException, http_exception_handler)
application.add_exception_handler(Exception.UnicornException, Exception.unicorn_exception_handler)
application.add_exception_handler(ValidationError, Exception.http422_exception_handler)
# 中间件

# 静态资源目录

app = application