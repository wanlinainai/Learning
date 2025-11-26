import uuid
from typing import Dict

from server.db import ConversationModel, MessageModel
from server.db.session import with_async_session


@with_async_session
async def add_message_to_db(
        session,
        user_id: str,
        conversation_id : str,
        conversation_name : str,
        prompt_name : str,
        query: str,
        response: str = "",
        metadata: Dict= {},
        message_id = None
):
    """
    新增聊天记录
    :param session: 
    :param user_id: 
    :param conversation_id: 
    :param conversation_name: 
    :param prompt_name: 
    :param query: 
    :param response: 无效参数
    :param metadata: 无效参数
    :param message_id: 
    :return: 
    """
    # 获取到会话
    conversation = await session.get(ConversationModel, conversation_id)
    
    if conversation is None:
        conversation = ConversationModel(
            id=conversation_id,
            user_id = user_id,
            name = conversation_name,
            chat_type = prompt_name
        )
        session.add(conversation)
    await session.commit()
    
    if not message_id:
        message_id = str(uuid.uuid4())
        
    # 创建MessageModel实例
    m=  MessageModel(
        id=message_id,
        conversation_id= conversation_id,
        chat_type = prompt_name,
        query=query,
        response = response,
        metadata = metadata
    )
    
    session.add(m)
    
    await session.commit()
    return m.id