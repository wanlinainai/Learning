import argparse
import asyncio
import sys
import multiprocessing as mp
import time
from multiprocessing import Process
from typing import Tuple, List, Dict

import uvicorn
from fastapi import FastAPI, Body
from fastchat.serve.openai_api_server import app_settings
from fastchat.utils import build_logger

from configs.basic_config import logger, LOG_PATH
from configs.model_config import LLM_MODELS
from configs.server_config import FSCHAT_MODEL_WORKERS, HTTPX_DEFAULT_TIMEOUT, FSCHAT_CONTROLLER, FSCHAT_OPENAI_API, \
    API_SERVER
from server.utils import get_httpx_client, fschat_controller_address, set_httpx_config, get_model_worker_config


def parse_args() -> Tuple[argparse.Namespace, argparse.ArgumentParser]:
    '''
    定义启动的模型、controller、Worker命令行
    :return:
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m',
        '--model-worker',
        action='store_true',
        help="run fastchat's model_worker server with specified model name. "
             "specify --model-name if not using default LLM_MODELS",
        dest='model_worker'
    )

    parser.add_argument(
        '-n',
        '--model-name',
        type=str,
        nargs='+',
        default=LLM_MODELS,
        help="specify model name for model worker."
            "add addition names with space seperated to start multiple model workers.",
        dest='model_name'
    )

    parser.add_argument(
        '-c',
        '--controller',
        type=str,
        help="specify controller address the worker is registered to default is FSCHAT_CONTROLLER",
        dest='controller_address'
    )

    args = parser.parse_args()
    return args, parser

def create_controller_app(
        dispatch_method: str,
        log_level: str = 'INFO'
) -> FastAPI:
    """
    :param dispatch_method: 调度方法，如何将请求分配给不同的模型工作器。
    :param log_level:日志级别
    :return:
    """
    import fastchat.constants
    fastchat.constants.LOGDIR = LOG_PATH
    from fastchat.serve.controller import app, Controller, logger
    logger.setLevel(log_level)

    controller = Controller(dispatch_method)
    sys.modules['fastchat.serve.controller'].controller = controller

    app.title = 'FastChat Controller'
    app._controller = controller
    return app


def _set_app_event(app: FastAPI, started_event: mp.Event = None):
    @app.on_event('startup')
    async def on_startup():
        if started_event is not None:
            started_event.set()


def run_controller(log_level: str = "INFO", started_event: mp.Event = None):
    """
    启动fastChat 的 controller，协调多个模型的工作进程（Model Worker）
    :return:
    """
    from server.utils import set_httpx_config
    set_httpx_config()

    app = create_controller_app(
        dispatch_method=FSCHAT_MODEL_WORKERS.get('dispatch_method'),
        log_level=log_level,
    )

    _set_app_event(app, started_event)

    @app.post('/release_worker')
    def release_worker(
            model_name: str = Body(..., description='释放模型的名称', samples=['chatglm-6b']),
            new_model_name: str = Body(None, description='释放之后加载的模型名称'),
            keep_origin: bool = Body(None, description="不释放模型，加载新的模型")
    ):
        available_models = app._controller.list_models()
        if new_model_name in available_models:
            msg = f'切换的模型{new_model_name}已经存在'
            logger.info(msg)
            return {"code": 500, 'msg': msg}

        if model_name not in available_models:
            msg = f'释放的模型{model_name}不存在'
            logger.error(msg)
            return {"code": 500, 'msg': msg}

        worker_address = app._controller.get_worker_address(model_name)
        if not worker_address:
            msg = f'can not find model_worker address of {model_name}'
            logger.error(msg)
            return {'code': 500, 'msg': msg}
        with get_httpx_client() as client:
            r = client.post(worker_address + '/release',
                            json={'new_model_name': new_model_name, 'keep_origin': keep_origin})
            if r.status_code != 200:
                msg = f'failed to release model: {model_name}'
                logger.error(msg)
                return {'code': 500, 'msg': msg}

        if new_model_name:
            timer = HTTPX_DEFAULT_TIMEOUT
            while timer > 0:
                models = app._controller.list_models()
                if new_model_name in models:
                    break
                time.sleep(1)
                timer -= 1
            if timer > 0:
                msg = f'success change model from {model_name} to {new_model_name}'
                logger.info(msg)
                return {"code": 200, "msg": msg}
            else:
                msg = f'failed to change model from {model_name} to {new_model_name}'
                logger.error(msg)
                return {'code': 500, 'msg': msg}
        else:
            msg = f'success to release model: {model_name}'
            logger.info(msg)
            return {'code': 200, "msg": msg}

    host = FSCHAT_CONTROLLER['host']
    port = FSCHAT_CONTROLLER['port']

    # 避免fastchat吞掉报错信息日志
    if log_level == 'ERROR':
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    uvicorn.run(app, host=host, port=port, log_level=log_level.lower())

def create_openai_api_app(
        controller_address: str,
        api_keys: List = [],
        log_level: str = 'INFO'
) -> FastAPI:
    """
    创建openai服务
    :param controller_address:
    :param api_keys:
    :param log_level:
    :return:
    """
    import fastchat.constants
    fastchat.constants.LOGDIR = LOG_PATH
    logger = build_logger('openai-api', "openai-api.log")
    logger.setLevel(log_level)

    from fastchat.serve.openai_api_server import app, CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=['*'],
        allow_mehtods=['*'],
        allow_headers=['*']
    )

    sys.modules['fastchat.serve.openai_api_server'].logger = logger
    app_settings.controller_address = controller_address
    app_settings.api_keys = api_keys

    app.title = 'FastChat Controller'
    return app

def run_openai_api(log_level:str = 'INFO', started_event: mp.Event = None):
    """
    FastChat启动 OpenAI API
    :return:
    """
    set_httpx_config()

    controller_addr = fschat_controller_address()
    app = create_openai_api_app(controller_addr, log_level=log_level)
    _set_app_event(app, started_event)

    host = FSCHAT_OPENAI_API['host']
    port = FSCHAT_OPENAI_API['port']

    if log_level == 'ERROR':
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
    uvicorn.run(app, host=host, port=port)

def create_model_worker_app(log_level: str = 'INFO', **kwargs) -> FastAPI:
    '''
    创建模型worker FastAPI服务
    :param log_level: 日志等级
    :param kwargs: 包含model_name、controller_address、worker_address、model_path
    :return:
    '''
    parser = argparse.ArgumentParser()
    args = parser.parse_args([])

    for k, v in kwargs.items():
        setattr(args, k, v)
    if worker_class :=kwargs.get('langchain_model'):
        worker = ''
    elif worker_class := kwargs.get('worker_class'):
        from fastchat.serve.base_model_worker import app
        worker = worker_class(
            model_names = args.model_names,
            controller_addr = args.controller_address,
            worker_addr = args.worker_address,
        )
        # Python的logging模块中获取logger之后通过setLevel设置日志等级
        sys.modules['fastchat.serve.base_model_worker'].logger.setLevel(log_level)

    # 本地环境
    else:
        pass

    app.title = f'FastChat LLM Server ({args.model_name[0]})'
    app._worker = worker
    return app


def run_model_worker(
        model_name: str = LLM_MODELS[0],
        controller_address: str = "",
        log_level: str = 'INFO',
        q: mp.Queue = None,
        started_event: mp.Event = None
):
    set_httpx_config()

    kwargs = get_model_worker_config(model_name)
    host = kwargs.pop('host')
    port = kwargs.pop('port')
    kwargs['model_name'] = [model_name]
    kwargs['controller_address'] = controller_address or fschat_controller_address()
    kwargs['worker_address'] = fschat_controller_address(model_name)
    model_path = kwargs.get('model_path', '')
    kwargs['model_path'] = model_path

    app = create_model_worker_app(log_level=log_level, **kwargs)
    _set_app_event(app, started_event)
    if log_level == 'ERROR':
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
    @app.post('/release')
    def release_model(
            new_model_name: str = Body(None, description="释放后加载该模型"),
            keep_origin: bool = Body(False, description='不释放原模型，加载新的模型')
    ) -> Dict:
        # 如果是不释放原模型的话，需要在Queue中加一条start 记录
        if keep_origin:
            if new_model_name:
                q.put([model_name, 'start', new_model_name])
        else:
            if new_model_name:
                q.put([model_name, 'replace', new_model_name])
            else:
                q.put([model_name, 'stop', None])
        return {'code': 200, 'msg': 'done!'}

    uvicorn.run(app, host=host, port=port, log_level=log_level.lower())

def run_api_server(started_event: mp.Event = None):
    """
    运行API 服务
    """
    app = create_app()
    _set_app_event(app, started_event)

    host = API_SERVER["host"]
    port = API_SERVER["port"]

    uvicorn.run(app, host=host, port=port)

async def start_main_server():
    import time
    import signal
    def handler(signalname):
        def f(signal_received, frame):
            # 优雅退出流程，和 kill 一样是退出流程
            raise KeyboardInterrupt(f'{signalname} received, exiting...')
        return f

    signal.signal(signal.SIGINT, handler("SIGINT"))
    signal.signal(signal.SIGTERM, handler("SIGTERM"))

    mp.set_start_method("spawn")
    manager = mp.Manager()

    queue = manager.Queue()
    args, parser = parse_args()

    logger.info(f'正在启动服务....')
    logger.info(f'若要查看日志内容，请前往：{LOG_PATH}')

    log_level = 'INFO'

    # 构建进程初始化信息
    processes = {'online_api': {}, "model_worker": {}}

    # 进程之间通知，通知是否启动完成
    controller_started = manager.Event()

    process = Process(
        target=run_controller,
        name=f'controller',
        kwargs=dict(log_level=log_level, started_event=controller_started),
        daemon=True
    )

    processes['controller'] = process

    process = Process(
        target=run_openai_api,
        name=f'openai_api',
        daemon=True
    )

    processes['openai_api'] = process

    model_worker_started = []
    # 启动在线和离线大模型（没有离线）
    for model_name in args.model_name:
        config = get_model_worker_config(model_name)
        if (config.get('online_api')
            and config.get('worker_class')
            and model_name in FSCHAT_MODEL_WORKERS):
            e = manager.Event()
            model_worker_started.append(e)
            # 启动在线模型进程
            process = Process(
                target=run_model_worker,
                name=f'api_worker - {model_name}',
                kwargs=dict(model_name=model_name,
                            controller_address=args.controller_address,
                            log_level=log_level,
                            q=queue,
                            started_event=e
                            ),
                daemon=True
            )
            processes['online_api'][model_name] = process
    api_started = manager.Event()

    process = Process(
        target=run_api_server,
        name=f'API server',
        kwargs=dict(started_event=api_started),
        daemon=True
    )

    processes['api'] = process

    pass

if __name__ == '__main__':
    # 运行一个异步事件循环，启动一个主服务器
    if sys.version_info < (3, 10):
        loop = asyncio.get_event_loop()

    else:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()

        asyncio.set_event_loop(loop)

    loop.run_until_complete(start_main_server())