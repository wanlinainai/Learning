import hashlib
import uuid


def random_str():
    """
    唯一随机字符串
    :return:
    """
    only = hashlib.md5(str(uuid.uuid1()).encode(encoding="utf-8")).hexdigest()
    return str(only)