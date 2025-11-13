import os
from pathlib import Path
from typing import Dict

from configs.basic_config import logger
from configs.kb_config import TEXT_SPLITTER_NAME

LOADER_DICT = {
    "UnstructuredMarkdownLoader": ['.md'],
    'JSONLoader': ['.json'],
    'JSONLinesLoader': ['.jsonl'],
    'UnstructuredLightPipeline': ['.pdf']
}
SUPPORTED_EXTS = [ext for sublist in LOADER_DICT.values() for ext in sublist ]


def get_kb_path(knowledge_base_name: str):
    return os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge_base"), knowledge_base_name)

def get_doc_path(knowledge_base_name: str):
    return os.path.join(get_kb_path(knowledge_base_name), 'content')

def get_file_path(knowledge_base_name: str, doc_name: str):
    doc_path = Path(get_doc_path(knowledge_base_name=knowledge_base_name)).resolve()
    file_path = (doc_path / doc_name).resolve()
    if str(file_path).startswith(str(doc_path)):
        return str(file_path)


def get_LoaderClass(file_extension):
    """
    根据文件扩展名得到加载器
    :param file_extension:
    :return:
    """
    for LoaderClass, extensions in LOADER_DICT.items():
        if file_extension in extensions:
            return LoaderClass



class KnowledgeFile:
    def __init__(
            self,
            filename: str,
            knowledge_base_name: str,
            loader_kwargs: Dict = {}
    ):
        """
        对应着知识库目录中的文件，需要是磁盘中存在才可以进行向量化
        """
        self.kb_name = knowledge_base_name
        self.filename = str(Path(filename).as_posix())
        self.ext = os.path.splitext(filename)[-1].lower()
        if self.ext not in SUPPORTED_EXTS:
            raise ValueError(f'暂未支持文档的格式: {self.ext}')
        self.loader_kwargs = loader_kwargs
        self.filepath = get_file_path(knowledge_base_name, filename)
        self.docs = None
        self.splited_docs = None
        self.document_loader_name = get_LoaderClass(self.ext)
        self.text_splitter_name = TEXT_SPLITTER_NAME

        # 打印看看属性
        print(f"知识库名称: {self.kb_name}")
        print(f"文件名: {self.filename}")
        print(f"文件扩展名: {self.ext}")
        print(f"加载器参数: {self.loader_kwargs}")
        print(f"文件路径: {self.filepath}")
        print(f"文档内容（初始值）: {self.docs}")
        print(f'拆分之后的文档内容（初始值）: {self.splited_docs}')
        print(f'文档加载器名称: {self.document_loader_name}')
        print(f"文本拆分器名称: {self.text_splitter_name}")

    def file2docs(self, refresh: bool = False):
        """
        将文件转换为文档
        refresh: 强制刷新
        :return:
        """
        if self.docs is None or refresh:
            logger.info(f"{self.document_loader_name} used for {self.filepath}")
            # 获取加载器，之后将文件内容进行加载
            # loader = get_loader(loader_name=self.document_loader_name, file_path=self.filepath, loader_kwargs=self.loader_kwargs)