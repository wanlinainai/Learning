from sqlalchemy import select
import asyncio
from server.db.session import with_async_session
from sqlAlchemyTest.test01 import Test


@with_async_session
async def get_all_user(session, name):
    test = await session.execute(
        select(Test)
        .where(Test.name.ilike(f"%{name}%"))
    )

    from sqlalchemy.dialects import mysql

    stmt = select(Test).where(Test.name.ilike(name))
    print(stmt.compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True}))

    test_info = test.scalars().first()

    return test_info



if __name__ == '__main__':
    result = asyncio.run(get_all_user(name="xu"))
    print("查询结果:" , result)