
import uuid

from datetime import datetime
from fastapi import Body, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from server.db import ConversationModel, MessageModel
from server.db.session import get_async_db
from fastapi.responses import JSONResponse


class CreateConversationRequest(BaseModel):
    user_id:str
    name: str
    chat_type: str

class ConversationResponse(BaseModel):
    id: str
    name: str
    chat_type: str
    create_time: datetime

class MessageResponse(BaseModel):
    id: str = Field(..., description="消息的唯一标识符号")
    conversation_id:str = Field(..., description="关联的会话ID")
    chat_type: str = Field(..., description="聊天类型")
    query: str = Field(..., description="用户查询的问题")
    response: str = Field(..., description="模型的响应回答")
    meta_data: dict = Field(..., description="其他元数据")
    feedback_score: int = Field(..., description="用户评分")
    feedback_reason: str = Field(..., description="评分理由")
    create_time:datetime =Field(..., description="消息创建时间")

# 创建新的会话
async def create_conversation(
        request: CreateConversationRequest = Body(...),
        session: AsyncSession = Depends(get_async_db)
):
    try:
        # 创建新的会话对象
        new_conversation =ConversationModel(
            id=str(uuid.uuid4()),
            user_id=request.user_id,
            name = request.name,
            chat_type=request.chat_type,
            create_time=datetime.now()
        )

        session.add(new_conversation)
        await session.commit()
        await session.refresh(new_conversation)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"id": new_conversation.id}
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Error creating conversation: {str(e)}')

# 获取用户的会话列表
async def get_user_conversations(
        user_id: str,
        session: AsyncSession = Depends(get_async_db)
):
    async with session as async_session:
        result = await async_session.execute(
            select(ConversationModel)
            .where(ConversationModel.user_id == user_id)
        )

        conversations = result.scalars().all()

        return [ConversationResponse(
            id=conv.id,
            name=conv.name,
            chat_type=conv.chat_type,
            create_time=conv.create_time
        ) for conv in conversations]

# 获取某一个会话id 消息列表
async def get_conversation_messages(
        conversation_id: str,
        session: AsyncSession = Depends(get_async_db)
):
    async with session as async_session:
        result = await async_session.execute(
            select(MessageModel)
            .where(MessageModel.conversation_id == conversation_id)
        )
        messages = result.scalars().all()

        return [MessageResponse(
            id=msg.id,
            conversation_id=msg.conversation_id,
            chat_type=msg.chat_type,
            query=msg.query,
            response=msg.response,
            meta_data=msg.meta_data,
            feedback_score=msg.feedback_score,
            feedback_reason=msg.feedback_reason,
            create_time=msg.create_time
        )for msg in messages]