from typing import List, Dict

from langchain_core.documents import Document

from server.db.repository.knowledge_base_repository import add_kb_to_db
from server.knowledge_base.kb_service.base import KBService
from server.knowledge_base.utils import get_kb_path, get_doc_path, KnowledgeFile


class FaissKBService(KBService):
    """
    FaissKBService是一个继承自基类的实例类，用于管理 FAISS 的知识库服务
    """
    vs_path: str  # 向量存储的文件路径
    kb_path: str  # 知识库文件的路径
    vector_name: str = None  # 向量名称，默认是None， 可以在初始化的时候设置

    def do_init(self):
        """
        初始化FAISS服务，设置向量名称、知识库路径和向量存储路径。
        :return:
        """
        self.vector_name = self.vector_name or self.embed_model
        self.kb_path = self.get_kb_path()
        self.vs_path = self.get_vs_path()

    def get_kb_path(self):
        """
        获取知识库文件的路径
        :return:
        """
        return get_kb_path(self.kb_name)

    def get_vs_path(self):
        """
        获取向量存储的文件路径
        :return:
        """
        return get_doc_path(self.kb_name)

    def _doc_to_embeddings(self, docs: List[Document]) -> Dict:
        """
        将List[Document]转成VectorStore.add_embeddings 可以接受的参数
        :return:
        """
        return embed_documents(docs=docs, embed_model=self.embed_model, to_query=False)

    async def do_add_doc(self,
                         docs: List[Document],
                         **kwargs) -> List[Dict]:
        """
        添加文档到向量数据库
        :return:
        """
        data = self._doc_to_embeddings(docs)  # 将向量化单独出来减少向量库的锁定时间




async def main():
    faissService = FaissKBService("test")
    print(f'faiss_kb_service: {faissService}')

    from server.knowledge_base.kb_service.base import KBServiceFactory
    kb = await KBServiceFactory.get_service_by_name("test")

    # 如果不存在该知识库，创建一个
    if kb is None:


        await add_kb_to_db(
            kb_name="test",
            kb_info='test',
            vs_type='faiss',
            embed_model="text-embedding-3-small",
            user_id="admin"
        )

    # 添加一个”READEME.md“文档，使用await
    await faissService.add_doc(KnowledgeFile("READEME.md", "test"))

    # 检索



if __name__ == '__main__':
    import asyncio
    asyncio.run(main())