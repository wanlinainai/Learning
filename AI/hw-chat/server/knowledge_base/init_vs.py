import asyncio
import os
from pathlib import Path

from document_loader.pdfloader import UnstructuredLightPipeline
from server.db.repository.knowledge_base_repository import add_kb_to_db
from server.knowledge_base.kb_service.faiss_kb_service import FaissKBService
from server.knowledge_base.utils import KnowledgeFile


async def process_and_add_document(file_path, faiss_service):

    # 获取知识库
    from server.knowledge_base.kb_service.base import KBServiceFactory
    kb = await KBServiceFactory.get_service_by_name("private")

    # 如果想要使用的向量数据库中的collecting name不存在，需要创建
    if kb is None:
        await add_kb_to_db(kb_name="private",
                           kb_info='private',
                           vs_type='faiss',
                           embed_model='bge-large-zh-v1.5',
                           user_id='admin')
    processer = UnstructuredLightPipeline()
    docs = await processer.run_pipeline(file_path, ['unstructured'])

    # 创建 KnowledgeFile 对象
    # Path Class ： 将路径包装成一个对象，其中可以直接使用各种方法：p.exists()  p.is_dir()  p.is_file()  p.parent  p.name  p.suffix
    kb_file = KnowledgeFile(Path(file_path).name, "private")

    # 添加文档到faiss
    added_docs_info = await faiss_service.add_doc(kb_file, docs)
    print(f'Added documents for {file_path}: {added_docs_info}')

async def main():
    """
    私有数据处理
    :return:
    """
    # 拿到对应的pdf文档
    folder_path = "/Users/a1234/Downloads/hw-chat-0.2/knowledge_base/private/content"
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
    # 实例化 FaissService
    faiss_service = FaissKBService("private")
    # 处理每一个 PDF 文件
    for pdf_file in pdf_files:
        full_path = os.path.join(folder_path, pdf_file)
        await process_and_add_document(full_path, faiss_service)

async def wiki_main():
    """
    wiki 数据处理
    :return:
    """


async def sequential_execution():

    await main()
    # await wiki_main()

async def test_query():
    faissService = FaissKBService("private")
    search_ans = await faissService.search_docs(query = 'GLM多角色对话系统解释')
    print(search_ans)

if __name__ == '__main__':
    # 数据入库
    asyncio.run(sequential_execution())
    # 测试看看
    asyncio.run(test_query())