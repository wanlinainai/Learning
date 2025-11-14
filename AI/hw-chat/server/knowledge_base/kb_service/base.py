import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, List

from langchain_core.documents import Document

from configs.kb_config import KB_INFO
from configs.model_config import EMBEDDING_MODEL
from server.db.repository.knowledge_base_repository import load_kb_from_db
from server.knowledge_base.utils import get_kb_path, get_doc_path, KnowledgeFile


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

    @abstractmethod
    def do_add_doc(self):
        pass

    async def add_doc(self, kb_file: KnowledgeFile, docs: List[Document] = [], **kwargs):
        """
        向知识库添加文件内容
        :param kb_file:
        :param docs:
        :param kwargs:
        :return:
        """
        if docs:
            custom_docs = True
            for doc in docs:
                doc.metadata.setdefault('source', kb_file.filename)
        else:

            # 执行文档加载 --> 文档切分两个过程
            docs = kb_file.file2text()
            custom_docs = False

        if docs:
            for doc in docs:
                try:
                    source = doc.metadata.get('source', '')
                    if os.path.isabs(source):
                        rel_path = Path(source).relative_to(self.doc_path)
                except Exception as e:
                    print(f'无法将绝对路径换成相对路径：{source}, error is {e}')

            # 添加到向量数据库
            doc_infos = await self.do_add_doc(docs, **kwargs)


class SupportedVSType:
    """
    SupportedVSType 是一个枚举类，表示支持的向量存储类型
    """
    FAISS = "faiss"
    PINECONE = "pinecone"
    MILVUS = "milvus"
    QDRANT = "qdrant"
    CHROMA = "chroma"
    DEFAULT = "default"


class KBServiceFactory:
    """
    KBServiceFactory 是一个工厂类，提供根据指定的向量存储类型获取到不同的数据库服务的方法
    """
    @staticmethod
    def get_service(
            kb_name: str,
            vector_store_type: Union[str, SupportedVSType],
            embed_model: str = EMBEDDING_MODEL
    ) -> KBService:
        """
        根据向量存储返回一个知识库服务
        :param kb_name:
        :param vector_store_type:
        :param embed_model:
        :return:
        """
        if isinstance(vector_store_type, str):
            vector_store_type = getattr(SupportedVSType, vector_store_type.upper())
        if SupportedVSType.FAISS == vector_store_type:
            from server.knowledge_base.kb_service.faiss_kb_service import FaissKBService
            return FaissKBService(kb_name, embed_model=embed_model)
        elif SupportedVSType.DEFAULT == vector_store_type:
            from server.knowledge_base.kb_service.faiss_kb_service import FaissKBService
            return FaissKBService(kb_name, embed_model=embed_model)
        # TODO：补充其他类型的支持库类型....

    @staticmethod
    async def get_service_by_name(kb_name: str) -> KBService:
        """
        根据支持库名称获取知识库服务
        :param kb_name:
        :return:
        """
        _, vs_type, embed_model = await load_kb_from_db(kb_name)
        if _ is None:
            return None
        return KBServiceFactory.get_service(kb_name, vs_type, embed_model=embed_model)