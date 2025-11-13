import logging
import os

import langchain
#  日志相关部分


## 是否详细显示日志
log_verbose = False
langchain.verbose = False


## 日志格式
LOG_FORMAT = "%(asctime)s - %(filename)s[line: %(lineno)d] - %(levelname)s: %(message)s"
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format=LOG_FORMAT)


## 日志存储路径
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
print(LOG_PATH)
if not os.path.exists(LOG_PATH): # 没有目录创建目录
    os.mkdir(LOG_PATH)
