from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from server.chat.chat import chat


def create_app():
    """
    创建一个 FastAPI 服务
    """
    app = FastAPI(title=f'hw_chat API Server')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 挂载路由
    mount_app_routes(app)

    # 挂载 VUE 构建前端的静态文件夹
    app.mount('/', StaticFiles(directory='static/dist'), name='static')
    return app


def mount_app_routes(app: FastAPI):
    """
    定义通用的接口访问地址
    """
    app.post('/api/chat',
             tags=['Chat'],
             summary='大模型对话交互接口')(chat)