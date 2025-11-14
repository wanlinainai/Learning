from fastchat.serve.base_model_worker import BaseModelWorker


class ApiModelWorker(BaseModelWorker):
    DEFAULT_EMBED_MODEL: str = None