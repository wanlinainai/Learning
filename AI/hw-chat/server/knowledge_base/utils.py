import importlib
import os
from pathlib import Path
from typing import Dict, List

import langchain.text_splitter
from langchain_core.documents import Document
from langchain_text_splitters import TextSplitter

from configs.basic_config import logger, log_verbose
from configs.kb_config import TEXT_SPLITTER_NAME, ZH_TITLE_ENHANCE, CHUNK_SIZE, OVERLAP_SIZE, text_splitter_dict
from configs.model_config import LLM_MODELS
from server.utils import get_model_worker_config
from text_splitter.zh_title_enhance import func_zh_title_enhance

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

def get_loader(loader_name: str, file_path: str, loader_kwargs: Dict = None):
    """
    根据loadername和文件路径返回文档加载器
    :return: loader实例
    """
    loader_kwargs = loader_kwargs or {}
    try:
        # 根据 loader_name 导入相应的文档加载器
        if loader_name in ["UnstructuredLightPipeline"]:
            document_loader_module = importlib.import_module("document_loaders")
        else:
            document_loader_module = importlib.import_module("langchain.document_loaders")
        DocumentLoader = getattr(document_loader_module, loader_name)
    except Exception as e:
        # 如果加载器导入失败，记录日志并将加载器设置成UnstructuredFileLoader
        msg = f"为文件{file_path}查找加载器{loader_name}时出错：{e}"
        logger.error(f"{e.__class__.__name__}: {msg}", exc_info=e if log_verbose else None)
        document_loader_module = importlib.import_module('langchain_community.document_loaders')
        DocumentLoader = getattr(document_loader_module, "UnstructuredFileLoader")

    loader = DocumentLoader(file_path, **loader_kwargs)
    return logger

def make_text_splitter(
            splitter_name: str = TEXT_SPLITTER_NAME,
            chunk_size: int = CHUNK_SIZE,
            chunk_overlap: int = OVERLAP_SIZE,
            llm_model: str = LLM_MODELS[0]
    ):
        """
        获取相应的分词器
        :param splitter_name: 分词器名称
        :param chunk_size: 分块大小
        :param chunk_overlap: 重叠区域大小
        :param llm_model: 大语言模型
        :return:
        """
        splitter_name = splitter_name or "SpacyTextSplitter"
        try:
            # 如果是Markdown格式分词器，需要按照headers_to_split_on特殊处理
            if splitter_name == 'MarkdownHeaderTextSplitter':
                headers_to_split_on = text_splitter_dict[splitter_name]['headers_to_split_on']
                text_splitter = langchain.text_splitter.MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
            else:
                try:
                    # 首先使用用户自定义的文本加载器
                    text_splitter_module = importlib.import_module('text_splitter')
                    TextSplitter = getattr(text_splitter_module, splitter_name)
                except:
                    # 如果没有，使用Langchain的分词模块
                    text_splitter_module = importlib.import_module('langchain.text_splitter')
                    TextSplitter = getattr(text_splitter_module, splitter_name)

                if text_splitter_dict[splitter_name]['source'] == 'tiktoken':
                    try:
                        text_splitter = TextSplitter.from_tiktoken_encoder(
                            encoding_name=text_splitter_dict[splitter_name]['tokenizer_name_or_path'],
                            pipeline="zh_core_web_sm",
                            chunk_size=chunk_size,
                            chunk_overlap=chunk_overlap
                        )
                    except:
                        # 失败的话使用纯tiktoken编码器，不再依赖spacy中文处理能力
                        text_splitter = TextSplitter.from_tiktoken_encoder(
                            encoding_name=text_splitter_dict[splitter_name]['tokenizer_name_or_path'],
                            chunk_size = chunk_size,
                            chunk_overlap = chunk_overlap
                        )
                elif text_splitter_dict[splitter_name]['source'] == 'huggingface':
                    if text_splitter_dict[splitter_name]["tokenizer_name_or_path"] == '':
                        config = get_model_worker_config(llm_model)
                        text_splitter_dict[splitter_name]['tokenizer_name_or_path'] = config.get('model_path')

                    if text_splitter_dict[splitter_name]['tokenizer_name_or_path'] == 'gpt2':
                        from transformers import GPT2TokenizerFast
                        from langchain.text_splitter import CharacterTextSplitter
                        tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')
                    else:
                        from transformers import AutoTokenizer
                        tokenizer = AutoTokenizer.from_pretrained(
                            text_splitter_dict[splitter_name]['tokenizer_name_or_path'],
                            trust_remote_code=True
                        )
                    text_splitter = TextSplitter.from_huggingface_tokenizer(
                        tokenizer=tokenizer,
                        chunk_size=chunk_size,
                        chunk_overlap=chunk_overlap
                    )
                else:
                    try:
                        text_splitter=  TextSplitter(
                            pipeline="zh_core_web_sm",
                            chunk_size=chunk_size,
                            chunk_overlap=chunk_overlap
                        )
                    except:
                        text_splitter = TextSplitter(
                            chunk_size=chunk_size,
                            chunk_overlap=chunk_overlap
                        )


        except Exception as e:
            print(e)
            text_splitter_module = importlib.import_module('langchain.text_splitter')
            TextSplitter = getattr(text_splitter_module, 'RecursiveCharacterTextSplitter')
            text_splitter = TextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )

        return text_splitter


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
            loader = get_loader(loader_name=self.document_loader_name, file_path=self.filepath, loader_kwargs=self.loader_kwargs)

            self.docs = loader.load()

        return self.docs


    def docs2texts(
            self,
            docs: List[Document] = None,
            zh_title_enhance: bool = True,
            refresh: bool = False,
            chunk_size: int = CHUNK_SIZE,
            chunk_overlap: int = OVERLAP_SIZE,
            text_splitter: TextSplitter = None,
    ):

        docs = docs or self.file2docs(refresh=refresh)
        if not docs:
            return []
        if self.ext not in ['.csv']:
            if text_splitter is None:
                text_splitter = make_text_splitter(
                    splitter_name = self.text_splitter_name,
                    chunk_size= chunk_size,
                    chunk_overlap = chunk_overlap
                )
            if self.text_splitter_name == 'MarkdownHeaderTextSplitter':
                docs = text_splitter.split_text(docs[0].page_content)
            else:
                docs = text_splitter.split_documents(docs)
        if not docs:
            return []

        print(f'文档切割案例:{docs[0]}')
        if zh_title_enhance:
            docs = func_zh_title_enhance(docs)
        self.splited_docs = docs
        return self.splited_docs

    def file2text(self,
                  zh_title_enhance: bool = ZH_TITLE_ENHANCE,
                  refresh: bool = False,
                  chunk_size: int = CHUNK_SIZE,
                  chunk_overlap: int = OVERLAP_SIZE,
                  text_splitter: TextSplitter = None
                  ):
        """
        文件转文本
        :param zh_title_enhance: bool 中文增强
        :param refresh:
        :param chunk_size:
        :param chunk_overlap:
        :param text_splitter:
        :return:
        """
        if self.splited_docs is None or refresh:
            docs = self.file2docs()
            self.splited_docs = self.docs2texts(
                docs = docs,
                zh_title_enhance = zh_title_enhance,
                refresh = refresh,
                chunk_size = chunk_size,
                chunk_overlap = chunk_overlap,
                text_splitter = text_splitter
            )

        return self.splited_docs
