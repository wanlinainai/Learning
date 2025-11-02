from fastapi import Request
from watchgod import awatch

from models.base import AccessLog


async def   write_access_log(req: Request, user_id: int, note: str = None):
    """
    写入日志
    :param req:
    :param user_id:
    :param note:
    :return:
    """
    data = {
        "user_id": user_id,
        "target_url": req.get("path"),
        "user_agent": req.headers.get("user-agent"),
        "request_params": {
            "method": req.method,
            "params": dict(req.query_params),
            "body": bytes(await req.body()).decode()
        },
        "ip": req.headers.get("x-forwarded-for"),
        "note": note
    }

    await AccessLog.create(**data)