from abc import ABC
from typing import Optional, Dict, Any, Tuple, List

from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.language_models import BaseLanguageModel
from langchain_core.memory import BaseMemory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, get_buffer_string
from pydantic import Field
from torchaudio.utils.sox_utils import get_buffer_size

from server.db.repository.message_repository import filter_message


class BaseChatMemory(BaseMemory, ABC):
    chat_memory: BaseChatMessageHistory = Field(default_factory=ChatMessageHistory)
    output_key: Optional[str] = None
    input_key: Optional[str] = None
    return_messages: bool = False

    def _get_input_output(
            self,
            inputs: Dict[str, Any],
            outputs: Dict[str, str],
    ) -> Tuple[str, str]:
        if self.input_key is None:
            pass
        else:
            prompt_input_key = self.input_key
        if self.output_key is None:
            if len(outputs) != 1:
                raise ValueError(f'One output key expected, got {outputs.keys()}')
            output_key = list(outputs.keys())[0]
        else:
            output_key = self.output_key
        return inputs[prompt_input_key], outputs[output_key]

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """
        Save Context from this conversation to buffer
        :param inputs:
        :param outputs:
        :return:
        """
        input_str, output_str = self._get_input_output(inputs, outputs)
        self.chat_memory.add_user_message(input_str)
        self.chat_memory.add_ai_message(output_str)

    def clear(self) -> None:
        """
        清除记忆
        :return:
        """
        self.chat_memory.clear()


class ConversationBufferDBMemory(BaseChatMemory):
    conversation_id: str
    human_prefix: str = 'Human'
    ai_prefix: str = "Assistant"
    llm: BaseLanguageModel
    memory_key: str = 'history'
    max_token_limit: int = 2000
    message_limit: int = 10

    async def buffer(self) -> List[BaseMessage]:
        messages = await filter_message(conversation_id=self.conversation_id, limit=self.message_limit)

        chat_messages: List[BaseMessage] = []
        for message in messages:
            chat_messages.append(HumanMessage(content=message.query))
            chat_messages.append(AIMessage(content=message.response))
        if not chat_messages:
            return []

        # 获取当前的长度：利用get_buffer_string将message转成字符串，之后利用get_num_tokens调用分词器获取Token
        current_buffer_length = self.llm.get_num_tokens(get_buffer_string(chat_messages))
        # 如果超过了最大的Token，需要进行修剪，把chat_messages中的消息进行删除，将删除的内容保存下来（可以之后做概括操作）
        if current_buffer_length > self.max_token_limit:
            pruned_memory = []
            while current_buffer_length > self.max_token_limit and chat_messages:
                pruned_memory.append(chat_messages.pop(0))
                current_buffer_length = self.llm.get_num_tokens(get_buffer_string(chat_messages))
        return chat_messages

    def memory_variables(self):
        print('开始加载memory_variables...')
        return [self.memory_key]


    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return {}

    async def aload_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:

        buffer = self.buffer()
        if getattr(self, 'return_messages', False):
            final_buffer = buffer
        else:
            final_buffer = get_buffer_string(
                buffer,
                human_prefix=self.human_prefix,
                ai_prefix=self.ai_prefix,
            )
        return {self.memory_key: final_buffer}

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        pass

    def clear(self) -> None:
        pass
