import sys

DEFAULT_BIND_HOST = '127.0.0.1' if sys.platform != 'win32' else '127.0.0.1'

# LLM 模型运行设备，auto自动检测
LLM_DEVICE = 'auto'

FSCHAT_MODEL_WORKERS = {
    # 默认的Model Worker 启动配置
    "default": {
        "host": DEFAULT_BIND_HOST,
        "port": 20002,
        "device": LLM_DEVICE
    },

    # 本地模型 需要配置启动的设备，CPU 或者 GPU
    "chatglm3-6b": {
        "device": 'cuda'
    },

    # 在线模型只需要配置Model Worker端口即可
    'zhipu-api': {
        "port": 21001
    }
}