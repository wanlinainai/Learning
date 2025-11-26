from typing import List

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from server.chat.chat import chat
from server.chat.knowledge_base_chat import knowledge_base_chat
from server.verify.utils import create_conversation, ConversationResponse, get_user_conversations, MessageResponse, \
    get_conversation_messages


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

    app.post('/api/chat/knowledge_base_chat',
             tags=['Chat'],
             summary='知识库对话'
             )(knowledge_base_chat)

    app.post('/api/conversations',
             tags=['Conversations'],
             summary="新建会话接口")(create_conversation)

    app.get('/api/users/{user_id}/conversations',
            response_model=List[ConversationResponse],
            tags=['Users'],
            summary='获取指定用户会话列表'
            )(get_user_conversations)

    app.get('/api/conversations/{conversation_id}/messages',
            response_model=List[MessageResponse],
            tags=['Messages'],
            summary='获取指定会话的消息列表'
            )(get_conversation_messages)