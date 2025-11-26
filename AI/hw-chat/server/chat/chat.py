import asyncio
import json
from typing import Union, List, Optional, AsyncIterable

from fastapi import Body
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from sse_starlette import EventSourceResponse

from configs.model_config import LLM_MODELS, TEMPERATURE
from server.callback_handler.ConversationCallbackHandler import ConversationCallbackHandler
from server.chat.util import History
from server.db.repository.message_repository import add_message_to_db
from server.memory.conversation_db_buffer_memory import ConversationBufferDBMemory
from server.utils import get_ChatOpenAI, get_prompt_template, wrap_done
from server.verify.check_user import check_user


async def chat(
        query: str = Body(..., description='用户输入', examples=['你好']),
        user_id: str = Body("", description='用户ID'),
        conversation_id: str = Body('', description='对话框id'),
        conversation_name: str = Body("", description="对话框名称"),
        history_len: int = Body(-1, description='从数据库中读取消息的数量'),
        history: Union[int, List[History]] = Body([], description='历史对话，设置成一个整数可以从数据库中读取历史消息',
                                                  examples=[[{
                                                      "role": "user",
                                                      "content": "你好，你是一个很傻很呆的AI智能机器人"
                                                  },
                                                      {
                                                          "role": "assistant",
                                                          "content": "好的，我是一个傻子AI机器人"
                                                      }]]),
        stream: bool = Body(True, description='流式输出'),
        model_name: str = Body(LLM_MODELS[0], description='LLM 模型名称'),
        temperature: float = Body(TEMPERATURE, description="LLM 采样温度", ge=0.0, le=2.0),
        max_tokens: Optional[int] = Body(None, description='限制LLM生成Token数量，默认None代表模型最大值'),
        prompt_name: str = Body('default', description='使用的prompt模板名称（在configs/prompt_config.py中配置）')
):
    """
    聊天接口
    :param query: 用户输入内容
    :param user_id: 用户ID
    :param conversation_id: 对话ID
    :param history_len: 如果是1，需要前端传过来的历史对话，-1从数据库中查询历史信息
    :param history: 前端传过来的当前会话ID
    :param stream: 是否是流式输出
    :param model_name: 大模型名称
    :param temperature: 采样温度
    :param max_tokens: 大模型最大输入限制
    :param prompt_name: 提示模板
    :return:
    """
    async def chat_iterator() -> AsyncIterable[str]:
        nonlocal history, max_tokens
        callback = AsyncIteratorCallbackHandler()
        callbacks = [callback]

        memory=  None

        # 用户校验
        await check_user(user_id)
        # 构造一个新的message_id 记录
        message_id = await add_message_to_db(
            user_id=user_id,
            conversation_id=conversation_id,
            conversation_name=conversation_name,
            prompt_name=prompt_name,
            query=query
        )

        conversation_callback = ConversationCallbackHandler(
            conversation_id=conversation_id,
            message_id=message_id,
            chat_type=prompt_name,
            query=query
        )

        callbacks.append(conversation_callback)

        # 检查max_token值是否正确
        if isinstance(max_tokens, int) and max_tokens <= 0:
            max_tokens = None

        # 获取模型
        model = get_ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            callbacks=callbacks
        )

        # 构造历史消息，优先使用前端传递的消息；使用Memory 必须 prompt 包含memory.memory_key 对应的变量；
        if history is None:
            pass
        elif conversation_id and history_len > 0:
            prompt = get_prompt_template("llm_chat", "with_history")
            chat_prompt = PromptTemplate.from_template(prompt)
            # 根据conversation_id 获取 message 列表拼凑 memory
            memory = ConversationBufferDBMemory(
                conversation_id=conversation_id,
                llm = model,
                message_limit = history_len
            )
        else:
            pass
        # 构造链
        chain = LLMChain(prompt=chat_prompt, llm=model, memory=memory)

        # 创建异步任务
        task = asyncio.create_task(wrap_done(
            chain.acall({"input": query}),
            callback.done
        ))

        # 流式处理和非流式处理
        if stream:
            async for token in callback.aiter():
                yield json.dumps(
                    {'text': token, 'message_id': message_id},
                    ensure_ascii=False
                )
        else:
            answer = ''
            async for token in callback.aiter():
                answer += token
            yield json.dumps(
                {'text': answer, "message_id": message_id},
                ensure_ascii=False
            )
        await task
    return EventSourceResponse(chat_iterator())