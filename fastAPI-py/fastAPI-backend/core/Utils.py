import hashlib
import random
import uuid

from passlib.handlers.pbkdf2 import pbkdf2_sha256


def random_str():
    """
    唯一随机字符串
    :return:
    """
    only = hashlib.md5(str(uuid.uuid1()).encode(encoding="utf-8")).hexdigest()
    return str(only)

def en_pass(psw: str):
    """
    密码加密
    :param psw:
    :return:
    """
    password = pbkdf2_sha256.hash(psw)
    return password

def check_pass(password: str, old: str):
    """
    密码校验
    :param password:
    :param old:
    :return:
    """
    check = pbkdf2_sha256.verify(password, old)
    if check:
        return True
    return False

def random_number(ln: int):
    """
    随机数字
    :param ln:
    :return:
    """
    code = ""
    for i in range(ln):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        code += ch

    return code