from abc import ABC, abstractmethod

from configs.kb_config import KB_INFO
from configs.model_config import EMBEDDING_MODEL
from server.knowledge_base.utils import get_kb_path, get_doc_path


class KBService(ABC):
    def __init__(self,
                 knowledge_base_name: str,
                 embed_model: str = EMBEDDING_MODEL   # 嵌入模型名称
                 ):
        self.kb_name = knowledge_base_name
        self.kb_info = KB_INFO.get(knowledge_base_name, f"关于{knowledge_base_name}的介绍")
        self.embed_model = embed_model
        self.kb_path = get_kb_path(self.kb_name)
        self.doc_path = get_doc_path(self.kb_name)
        self.do_init()


    @abstractmethod
    def do_init(self):
        pass
