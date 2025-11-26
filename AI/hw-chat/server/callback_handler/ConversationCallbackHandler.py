from typing import Dict, Any

from langchain_core.callbacks import BaseCallbackHandler


# 回调处理类
class ConversationCallbackHandler(BaseCallbackHandler):
    raise_error: bool = True
    
    def __init__(self, conversation_id: str, message_id: str, chat_type: str, query: str):
        self.conversation_id = conversation_id
        self.message_id = message_id
        self.chat_type = chat_type
        self.query = query
        
    @property
    def always_verbose(self) -> bool:
        """
        只读属性，显示一些关键配置信息
        :return: 
        """
        return True
    
    def on_llm_start(
            self,
            serialized: Dict[str, Any],
            prompts: List[str],
            **kwargs: Any
    ) -> None:
        pass
    
    