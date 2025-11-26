import asyncio
import logging
import os
from typing import Any, List, Dict, Union, Callable, Optional, Awaitable

import httpx
import pydantic
from langchain_openai import ChatOpenAI
from mpmath import isint
from pydantic import BaseModel

from configs.basic_config import logger, log_verbose
from configs.model_config import MODEL_PATH, ONLINE_LLM_MODEL, LLM_MODELS
from configs.server_config import FSCHAT_MODEL_WORKERS, HTTPX_DEFAULT_TIMEOUT, FSCHAT_CONTROLLER, FSCHAT_OPENAI_API
from server import model_workers
from server.minx_chat_openai import MinxChatOpenAI


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

def fschat_controller_address() -> str:
    host = FSCHAT_CONTROLLER['host']
    if host == '0.0.0.0':
        host = '127.0.0.1'
    port = FSCHAT_CONTROLLER['port']
    return f'http://{host}:{port}'

def fschat_model_worker_address(model_name: str = LLM_MODELS[0]) -> str:
    if model := get_model_worker_config(model_name):
        host = model['host']
        if host == '0.0.0.0':
            host = '127.0.0.1'
        port = model['port']
        return f'http://{host}: {port}'
    return ''

def fschat_openai_api_address() -> str:
    '''
    获取OpenAI的 接口访问地址
    :return:
    '''
    host = FSCHAT_OPENAI_API['host']
    if host == '0.0.0.0':
        host = '127.0.0.1'
    port = FSCHAT_OPENAI_API['port']
    return f'http://{host}:{port}/v1'

def get_ChatOpenAI(
        model_name: str,
        temperature: float,
        max_tokens: int = None,
        streaming: bool = True,
        callbacks: List[Callable] = [],
        verbose: bool = True,
        **kwargs: Any
) -> ChatOpenAI:
    """
    创建 ChatOpenAI 实例的函数，在参数中自定义一些常用参数
    :param model_name:
    :param temperature:
    :param max_tokens:
    :param streaming:
    :param callbacks:
    :param verbose:
    :param kwargs:
    :return:
    """
    config = get_model_worker_config(model_name)
    # 修改编码器
    ChatOpenAI._get_encoding_model = MinxChatOpenAI.get_encoding_model
    model = ChatOpenAI(
        streaming=streaming,
        verbose=verbose,
        callbacks=callbacks,
        openai_api_key=config.get('api_key', "EMPTY"),
        openai_api_base=config.get('api_base_url', fschat_openai_api_address()),
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        openai_proxy=config.get('openai_proxy', None),
        **kwargs,
    )

    return model

def set_httpx_config(
        timeout: float = HTTPX_DEFAULT_TIMEOUT,
        proxy: Union[str, Dict] = None
):
    '''
    设置默认httpx超时时间和代理服务
    :param timeout: 超时时间，单位秒
    :param proxy: 代理
    :return:
    '''
    import httpx
    import os

    httpx._config.DEFAULT_TIMEOUT_CONFIG.connect = timeout
    httpx._config.DEFAULT_TIMEOUT_CONFIG.read = timeout
    httpx._config.DEFAULT_TIMEOUT_CONFIG.write = timeout

    # 在进程范围中设置系统代理
    proxies = {}
    if isinstance(proxy, str):
        for n in ['http', 'https', 'all']:
            proxies[n + '_proxy'] = proxy
    elif isinstance(proxy, dict):
        for n in ['http', 'https', 'all']:
            if p := proxy.get(n):
                proxies[n + '_proxy'] = p
            elif p:= proxy.get(n + '_proxy'):
                proxies[n + '_proxy'] = p

    for k, v in proxies.items():
        os.environ[k] = v

    no_proxy = [x.strip() for x in os.environ.get('no_proxy', '').split(',') if x.strip()]
    no_proxy += [
        'http://127.0.0.1',
        'http://localhost'
    ]

    # 不使用代理使用部署的FastChat服务
    for x in [
        fschat_controller_address(),
        fschat_model_worker_address(),
        fschat_openai_api_address()
    ]:
        host = ':'.join(x.split(':')[:2])
        if host not in no_proxy:
            no_proxy.append(host)
        os.environ["NO_PROXY"] = ','.join(no_proxy)

    # 修改默认的getproxies函数
    def _get_proxies():
        return proxies
    import urllib.request
    urllib.request.getproxies = _get_proxies()


def get_httpx_client(
        use_async: bool = False,
        proxies: Union[str, Dict] = None,
        timeout: float = HTTPX_DEFAULT_TIMEOUT,
        **kwargs,
) -> Union[httpx.Client, httpx.AsyncClient]:
    default_proxies = {
        'all://127.0.0.1': None,
        'all://localhost': None,
    }

    for x in [
        fschat_controller_address(),
        fschat_model_worker_address(),
        fschat_openai_api_address(),
    ]:
        host = ':'.join(x.split(':')[:2])
        default_proxies.update({host: None})

    default_proxies.update({
        "http://": (os.environ.get('http_proxy')
                    if os.environ.get('http_proxy') and len(os.environ.get('http_proxy').strip())
                    else None),
        "https://": (os.environ.get('https_proxy')
                     if os.environ.get("https_proxy") and len(os.environ.get('https_proxy').strip())
                     else None),
        "all://": (os.environ.get('all_proxy')
                   if os.environ.get('all_proxy') and len(os.environ.get('all_proxy').strip())
                   else None)
    })

    for host in os.environ.get('no_proxy', '').split(','):
        if host := host.strip():
            default_proxies.update({'all://' + host: None})

    if isinstance(proxies, str):
        proxies = {'all://': proxies}
    if isinstance(proxies, dict):
        default_proxies.update(proxies)

    kwargs.update(timeout=timeout, proxies=default_proxies)

    if log_verbose:
        logger.info(f'{get_httpx_client.__class__.__name__}: kwargs={kwargs}')

    if use_async:
        return httpx.AsyncClient(**kwargs)
    else:
        return httpx.Client(**kwargs)


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
    config.update(ONLINE_LLM_MODEL.get(model_name, {}).copy())
    config.update(FSCHAT_MODEL_WORKERS.get(model_name, {}).copy())

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

def get_prompt_template(type: str, name: str) -> Optional[str]:
    '''
    从prompt_config 中加载模板内容
    :param type: 模型类型：llm_chat、knowledge_base_chat
    :param name:
    :return:
    '''
    from configs import prompt_config
    # 热启动
    import importlib
    importlib.reload(prompt_config)
    return prompt_config.PROMPT_TEMPLATES[type].get(name)

async def wrap_done(fn: Awaitable, event: asyncio.Event):
    log_verbose = False

    try:
        await fn
    except Exception as e:
        logging.exception(e)
        msg = f'发生异常: {e}'
        logger.error(f'{e.__class__.__name__}: {msg}',
                     exc_info=e if log_verbose else None)
    finally:
        event.set()