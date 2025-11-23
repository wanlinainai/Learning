import argparse
import asyncio
import sys
import multiprocessing as mp
from multiprocessing import Process
from typing import Tuple

from configs.basic_config import logger, LOG_PATH
from configs.model_config import LLM_MODELS


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

def run_controller(log_level: str = "INFO", started_event: mp.Event = None):
    """
    启动fastChat 的 controller，协调多个模型的工作进程（Model Worker）
    :return:
    """
    # todo : Need todo
    pass

def run_openai_api():
    """
    FastChat启动 OpenAI API
    :return:
    """
    # todo : Need todo 
    pass

def start_main_server():
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