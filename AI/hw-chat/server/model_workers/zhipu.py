from typing import List, Literal

from server.model_workers import ApiModelWorker


class ChatGLMWorker(ApiModelWorker):
    DEFAULT_EMBED_MODEL = 'embedding-2'

    def __init__(
            self,
            *,
            model_names: List[str] = ('zhipu-api',),
            controller_addr: str = None,
            worker_addr: str = None,
            version: Literal['glm-4'] = 'glm4',
            **kwargs,
    ):
        kwargs.update(model_names=model_names, controller_addr=controller_addr, worker_addr= worker_addr)
        kwargs.setdefault('context_len', 4096)
        super().__init__(**kwargs)
        self.version = version