from typing import List, Optional, AsyncIterator

from fastapi import Body, Request
from langchain.callbacks import AsyncIteratorCallbackHandler
from sse_starlette import EventSourceResponse

from configs.kb_config import VECTOR_SEARCH_TOP_K, SCORE_THRESHOLD
from configs.model_config import LLM_MODELS, TEMPERATURE
from server.callback_handler.ConversationCallbackHandler import ConversationCallbackHandler
from server.chat.util import History
from server.db.repository.message_repository import add_message_to_db
from server.knowledge_base.kb_service.base import KBServiceFactory
from server.utils import BaseResponse


async def knowledge_base_chat(
        query:str = Body(..., description="用户输入", examples=['你好']),
        user_id: str = Body("", description="用户ID"),
        conversation_id: str = Body("", description="对话框id"),
        conversation_name: str = Body("", description="对话框名称"),
        knowledge_base_name: str = Body(..., description="知识库名称", examples=['samples']),
        top_k: int = Body(VECTOR_SEARCH_TOP_K, description="匹配向量数"),
        history: List[History] = Body(
            [],
            description="历史对话",
            examples=[[
                {"role": "user", "content": "你是谁?"},
                {"role": "assistant", "content": "我是一个傻傻的AI人工智能机器人"}
            ]]
        ),
        score_threshold: float = Body(
            SCORE_THRESHOLD,
            description="知识库匹配相关度阈值，取值范围是0 - 1，SCROE越小，相关度越高，尽可能折中 0.5 ",
            ge=0,
            le=2
        ),
        stream: bool = Body(False, description="流式输出"),
        model_name: str = Body(LLM_MODELS[0], description="LLM 模型名称"),
        temperature: float = Body(TEMPERATURE, description="LLM 采样温度", ge=0.0, le=1.0),
        max_tokens: Optional[int] = Body(None, description="限制LLM生成Token数量，默认NONE代表模型最大值"),
        prompt_name: str = Body("default", description="使用的Prompt模板名称(位置：configs/prompt_config.py中配置)"),
        request: Request = None
):
    """
    根据知识库回答问题
    :return:
    """

    # 提取向量数据库实例
    kb = await KBServiceFactory.get_service_by_name(knowledge_base_name)
    if kb is None:
        return BaseResponse(code=404, msg=f"未找到知识库{knowledge_base_name}")
    async def knowledge_base_chat_iterator(
            query: str,
            top_k: int = VECTOR_SEARCH_TOP_K,
            model_name: str = LLM_MODELS[0],
            prompt_name: str = ""
    ) -> AsyncIterator[str]:
        
        # 大模型回答之后回调
        callback = AsyncIteratorCallbackHandler()
        callbacks = [callback]
        
        # 数据库中新增一条message_id信息，通过回调将AI的回答信息保存到数据库
        message_id = await add_message_to_db(
            user_id = user_id,
            conversation_id = conversation_id,
            conversation_name = conversation_name,
            prompt_name = prompt_name,
            query = query,
        )
        
        conversation_callback = ConversationCallbackHandler(
            conversation_id = conversation_id,
            message_id = message_id,
            chat_type = prompt_name,
            query = query,
        )
        callbacks.append(conversation_callback)

        # 获取OpenAI模型信息

        # 检索文档（重点）

        # prompt模板处理（如果没有找到模板，使用空的Prompt模板；否则使用其他模版）

        # 历史消息

        # 构建Chain

        # 创建后台任务，chain.acall()方法

        # 修饰一下docs 最终输出：出处：索引数、文件名、地址 + 模型回答内容

        # 如果源文档没有内容，返回大模型自身回答

        # 通过stream参数判断返回的是流式返回还是非流式返回
    
    return EventSourceResponse(knowledge_base_chat_iterator(query, top_k, model_name, prompt_name))