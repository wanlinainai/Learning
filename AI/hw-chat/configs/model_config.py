from dotenv import load_dotenv
import os

load_dotenv()


# 选用的Embedding模型
EMBEDDING_MODEL = "text-embedding-3-small" # 价格便宜： 输入价格：$0.02，输出：$0.02

# 大语言模型
LLM_MODELS = ["zhipu-api"]
# "chatglm3-6b",

# 本地化模型
MODEL_PATH = {
    # 本地化大语言模型
    "local_model": {
        "chatglm3-6b": "/root/GLM/data/ZhipuAI/chatglm3-6b",
    },

    # 本地化embedding模型
    "embed_model": {
        "bge-large-zh-v1.5": '/root/GLM/data/ai-modelscope/bge-large-zh-v1___5'
    }
}

# 在线LLM 大模型
ONLINE_LLM_MODEL = {
    "zhipu-api": {
        "api-key": os.getenv("ZHIPU_API_KEY", ''),
        'version': os.getenv("ZHIPU_VERSION", ''),
        'provider': os.getenv("ZHIPU_PROVIDER", '')
    },

    "openai-api": {
        'model_name': os.getenv("OPENAI_MODEL_NAME", 'gpt-4o-mini'),
        'api_base_url': os.getenv("OPENAI_API_BASE_URL", ''),
        'api_key': os.getenv("OPENAI_API_KEY", ''),
        'openai_proxy': os.getenv("OPENAI_PROXY", '')
    }
}