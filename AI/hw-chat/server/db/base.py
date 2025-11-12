from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker

from configs.kb_config import SQLALCHEMY_DATABASE_URI

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=True # 开启日志
)

AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

Base: DeclarativeMeta = declarative_base()