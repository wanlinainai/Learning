from typing import Union, List, Optional, AsyncIterable

from fastapi import Body
from sse_starlette import EventSourceResponse

from configs.model_config import LLM_MODELS, TEMPERATURE
from server.chat.util import History


async def chat(
        query: str = Body(..., description='用户输入', examples=['你好']),
        user_id: str = Body("", description='用户ID'),
        conversation_id: str = Body('', description='对话框id'),
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
        pass

    return EventSourceResponse(chat_iterator())