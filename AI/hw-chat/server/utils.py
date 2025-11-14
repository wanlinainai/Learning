from typing import Any, List, Dict

import pydantic
from pydantic import BaseModel

from configs.model_config import MODEL_PATH, ONLINE_LLM_MODEL
from configs.server_config import FSCHAT_MODEL_WORKERS


class BaseResponse(BaseModel):
    code: int = pydantic.Field(200, description="API status code")
    msg: str = pydantic.Field("success", description="API status message")
    data: Any = pydantic.Field(None, description="API data")

    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "success"
            }
        }

def list_embed_models() -> List[str]:
    """
    得到配置中的本地化模型
    :return:
    """
    return list(MODEL_PATH['embed_model'])

def list_online_embed_models() -> List[str]:
    """
    得到配置中的在线大模型
    :return:
    """
    from server import model_workers
    ret = []
    for k, v in list_config_llm_models()['online'].items():
        if provider := v.get('provider'):
            # 在提供的提供商中找到对应服务类
            worker_class = getattr(model_workers, provider, None)
            if worker_class is not None and worker_class.can_embedding():
                ret.append(k)

def list_config_llm_models() -> List[str, Dict]:
    workers = FSCHAT_MODEL_WORKERS.copy()
    workers.pop('default', None)

    return {
        "local": MODEL_PATH["local_model"].copy(),
        "online": ONLINE_LLM_MODEL.copy(),
        "worker": workers
    }