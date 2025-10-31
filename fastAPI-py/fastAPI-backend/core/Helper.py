import hashlib
import uuid

"""
@description 工具函数
"""
def random_str():
    """
    唯一的随机字符串
    :return:
    """
    only = hashlib.md5(str(uuid.uuid1()).encode(encoding="utf-8")).hexdigest()
    return str(only)