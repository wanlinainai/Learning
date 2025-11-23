import os
import numpy as np
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, List

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from configs.kb_config import KB_INFO, VECTOR_SEARCH_TOP_K, SCORE_THRESHOLD
from configs.model_config import EMBEDDING_MODEL
from server.db.repository.knowledge_base_repository import load_kb_from_db
from server.db.repository.knowledge_file_repository import do_add_to_db
from server.embeddings_api import embed_texts, aembed_texts
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

    async def search_docs(
            self,
            query: str,
            top_k: int = VECTOR_SEARCH_TOP_K,
            score_threshold: float = SCORE_THRESHOLD
    ) -> List[Document]:
        """
        检索文档
        :return:
        """
        docs = await self.do_search(query, top_k, score_threshold)
        return docs

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
                        doc.metadata['source'] = str(rel_path.as_posix().strip('/'))
                except Exception as e:
                    print(f'无法将绝对路径换成相对路径：{source}, error is {e}')

            # 添加到向量数据库
            doc_infos = await self.do_add_doc(docs, **kwargs)
            status = await do_add_to_db(
                kb_file,
                custom_docs=custom_docs,
                docs_count= len(docs),
                doc_infos = doc_infos
            )
        else:
            status = False
        return status


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

def normalize(embeddings: List[List[float]]) -> np.ndarray:
    '''
    向量归一化，通过归一化，余弦相似度变成更加简单的点积。消除了对不同输入长度文本差异化
    :param embeddings:
    :return:
    '''
    norm = np.linalg.norm(embeddings, axis=1)
    norm = np.reshape(norm, (norm.shape[0], 1))
    norm = np.tile(norm, (1, len(embeddings[0])))
    return np.divide(embeddings, norm)

class EmbeddingsFunAdapter(Embeddings):
    def __init__(self, embed_model: str = EMBEDDING_MODEL):
        self.embed_model = embed_model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = embed_texts(texts=texts, embed_model=self.embed_model, to_query=False).data
        return normalize(embeddings).tolist()

    def embed_query(self, text: str) -> List[float]:
        embeddings = embed_texts(texts=[text], embed_model=self.embed_model, to_query=True).data
        query_embed = embeddings[0]
        query_embed_2d = np.reshape(query_embed, (1, -1))
        normalized_query_embed = normalize(query_embed_2d)
        return normalized_query_embed[0].tolist() # 结果转成一维数组之后返回

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = (await aembed_texts(texts=texts, embed_model=self.embed_model, to_query=False)).data
        return normalize(embeddings).tolist()

    async def aembed_query(self, text: str) -> List[float]:
        '''
        标准优化手段进行文本向量匹配
        :param text:
        :return:
        '''
        embeddings = (await aembed_texts(texts=[text], embed_model=self.embed_model, to_query=True)).data
        query_embed = embeddings[0]
        query_embed_2d = np.reshape(query_embed, (1, -1)) # 转成二维数组
        normalized_query_embed = normalize(query_embed_2d)
        return normalized_query_embed[0].tolist() # numpy数组准成Python数组