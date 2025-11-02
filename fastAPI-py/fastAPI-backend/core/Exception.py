"""
@Description 异常处理
"""
from typing import Union

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from tortoise.exceptions import ValidationError


async def http_exception_handler(_: Request, exec: HTTPException):
    """
    http 异常处理
    :param _:
    :param exec:
    :return:
    """
    if exec.status_code == 401:
        return JSONResponse(content={"detail": exec.detail}, status_code=exec.status_code)
    return JSONResponse({
        "code": exec.status_code,
        "message": exec.detail,
        "data": None
    }, status_code=exec.status_code, headers=exec.headers)


"""
@Description 自定义的Unicorn异常
"""
class UnicornException(Exception):
    def __init__(self, code, errmsg, data=None):
        """
        失败返回的格式
        :param self:
        :param code:
        :param errmsg:
        :param data:
        :return:
        """
        if data is None:
            data = {}
        self.code = code
        self.errmsg = errmsg
        self.data = data

async def unicorn_exception_handler(request: Request, exec: UnicornException):
    """
    自定义的Unicorn异常处理
    :param request:
    :param exec:
    :return:
    """
    return JSONResponse({
        "code": exec.code,
        "message": exec.errmsg,
        "data": exec.data
    }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

async def http422_exception_handler(request: Request, exec: Union[RequestValidationError, ValidationError]) -> JSONResponse:
    """
    参数校验异常
    :param request:
    :param exec:
    :return:
    """
    return JSONResponse({
        "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "message": exec.errors(),
        "data": None
    }, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    全局异常处理器 - 捕获所有未处理的异常
    :param request:
    :param exc:
    :return:
    """
    import traceback
    import logging

    # 记录详细的错误日志到后端
    logging.error(f"Global exception handler caught: {exc}")
    logging.error(traceback.format_exc())

    # 返回给前端的通用错误信息（不包含敏感的堆栈信息）
    return JSONResponse({
        "code": 500,
        "message": "服务器内部错误，请联系管理员",
        "data": None
    }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)