from server.knowledge_base.kb_service.base import KBService
from server.knowledge_base.utils import get_kb_path, get_doc_path

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