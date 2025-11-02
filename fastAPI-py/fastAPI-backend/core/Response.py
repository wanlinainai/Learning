from typing import List


def base_response(code, msg, data=None):
    if data is None:
        data = []
    result = {
        "code": code,
        "msg": msg,
        "data": data
    }
    return result

def success(data=None, msg=""):
    return base_response(200, msg, data)

def fail(data=None, msg="", code=-1):
    return base_response(code, msg, data)

"""
Ant design Table返回格式
"""
def res_antd(data: List = None, total: int = 0, code: bool = True):
    if data is None:
        data = []

    result = {
        "success": code,
        "data": data,
        "total": total
    }
    return result