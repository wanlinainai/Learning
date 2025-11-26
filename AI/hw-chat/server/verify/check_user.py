from fastapi import HTTPException

from server.db import UserModel
from server.db.session import with_async_session


@with_async_session
async def check_user(session, user_id: str):
    print('================')
    print(user_id)
    result=  await session.get(UserModel, user_id)
    if not result:
        raise HTTPException(status_code=401, detail='没有该用户')
    return {"message": "success"}