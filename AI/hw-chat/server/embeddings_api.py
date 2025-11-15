from typing import Dict, List

from langchain_core.documents import Document

from configs.model_config import EMBEDDING_MODEL
from server.utils import BaseResponse, list_embed_models, list_online_embed_models


def embed_texts(texts: List[str],
                embed_model: str = EMBEDDING_MODEL,
                to_query: bool = False) -> BaseResponse:
    """
    对文本进行向量化，返回数据格式：BaseResponse(data = List[List[float]])
    :return:
    """
    try:
        if embed_model in list_embed_models():  # 使用本地化向量模型
            pass
        if embed_model in list_online_embed_models():  # 使用在线向量模型
            # todo continue
            return BaseResponse(data=[])
    except Exception as e:
        return BaseResponse(code=500, msg=f"embedding error: {e}")


def embed_documents(
        docs: List[Document],
        embed_model: str = EMBEDDING_MODEL,
        to_query: bool = False
) -> Dict:
    """
    将List[Document]向量化，转成 VectorStore.add_embeddings 可接受的参数
    :return:
    """
    texts = [x.page_content for x in docs]
    metadatas = [x.metadata for x in docs]
    embeddings = embed_texts(texts=texts, embed_model=embed_model, to_query=to_query).data
    if embeddings is not None:
        return {
            "texts": texts,
            "embeddings": embeddings,
            "metadatas": metadatas
        }