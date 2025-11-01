from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from tortoise.exceptions import ValidationError

from config import settings
from core.Events import startup, stopping
from core import Exception, Middleware, Router
from api.Base import router

application = FastAPI(
    debug=settings.APP_DEBUG,
    docs_url="/docs",  # 启用 Swagger UI，使用默认路径
    redoc_url="/redoc",  # 启用 ReDoc
)

# 事件监听
application.add_event_handler("startup", startup(application))
application.add_event_handler("shutdown", stopping(application))

# 异常错误处理
application.add_exception_handler(HTTPException, Exception.http_exception_handler)
application.add_exception_handler(Exception.UnicornException, Exception.unicorn_exception_handler)
application.add_exception_handler(ValidationError, Exception.http422_exception_handler)

# 中间件
application.add_middleware(Middleware.BaseMiddleware)
application.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
application.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# 路由
application.include_router(Router.router)

# 静态资源目录
application.mount('/static', StaticFiles(directory=settings.STATIC_DIR), name="static")

app = application