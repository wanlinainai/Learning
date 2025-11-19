import os
from typing import Any, List, Dict

import pydantic
from pydantic import BaseModel

from configs.basic_config import logger, log_verbose
from configs.model_config import MODEL_PATH, ONLINE_LLM_MODEL
from configs.server_config import FSCHAT_MODEL_WORKERS
from server import model_workers


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

def list_config_llm_models() -> Dict[str, Dict]:
    workers = FSCHAT_MODEL_WORKERS.copy()
    workers.pop('default', None)

    return {
        "local": MODEL_PATH["local_model"].copy(),
        "online": ONLINE_LLM_MODEL.copy(),
        "worker": workers
    }

def get_model_worker_config(model_name: str = None) -> dict:
    """
    获取模型配置信息工具方法
    :param model_name: 模型名称，对应厂商模型对应表格找即可
    :return: 包含模型信息的字典
    """
    # 模型配置信息添加到dict中，update方法如果dict存在就更新，否则新增内容
    config = FSCHAT_MODEL_WORKERS.get('default', {}).copy()
    config.update(ONLINE_LLM_MODEL.get(model_name), {}).copy()
    config.update(FSCHAT_MODEL_WORKERS.get(model_name), {}).copy()

    # 如果传入的模型是本地部署的
    if model_name in MODEL_PATH['local_model']:

        local_model_path = MODEL_PATH['local_model'][model_name]
        if local_model_path and os.path.isdir(local_model_path):
            config['model_path_exists'] = True
        config['model_path'] = local_model_path
    # 如果传入的模型是在线的
    if model_name and model_name in ONLINE_LLM_MODEL:
        config['online_api'] = True
        if provider := config.get("provider"):
            try:
                config['worker_class'] = getattr(model_workers, provider)
            except Exception as e:
                msg = f'在线模型 ‘{model_name}’ 的provider没有正确配置，请检查'
                logger.error(f'{e.__class__.__name__}: {msg}', exc_info=e if log_verbose else None)
    return config