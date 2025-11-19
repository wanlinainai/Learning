import asyncio
import uuid
from typing import List

from fastchat.serve.base_model_worker import BaseModelWorker


class ApiModelWorker(BaseModelWorker):
    DEFAULT_EMBED_MODEL: str = None

    def __init__(
            self,
            model_names: List[str],
            controller_addr: str = None,
            worker_addr: str = None,
            context_len: int = 2048,
            no_register: bool = False,
            **kwargs,
    ):
        kwargs.setdefault('worker_id', uuid.uuid4().hex[:8])
        kwargs.setdefault('model_path', '')
        kwargs.setdefault('limit_worker_concurrency', 5)
        super().__init__(
            model_names=model_names,
            controller_addr=controller_addr,
            worker_addr=worker_addr,
            **kwargs
        )

        import fastchat.serve.base_model_worker
        import sys
        self.logger = fastchat.serve.base_model_worker.logger

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)

        self.context_len = context_len
        self.semaphore = asyncio.Semaphore(self.limit_worker_concurrency)
        self.version = None

        if not no_register and self.controller_addr:
            self.init_heart_beat()