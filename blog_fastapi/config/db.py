from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from sqlalchemy import (
    create_engine, Column, Integer, String, Text, DateTime,
    Enum, ForeignKey, Index, UniqueConstraint
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional, List

username = "root"
password = "123456"
host = "127.0.0.1"
port = "3306"
db = "personal_blog"

ASYNC_DATABASE_URL = f"mysql+aiomysql://{username}:{password}@{host}:{port}/{db}?charset=utf8mb4"



# ASYNC_DATABASE_URL = f"mysql+aiomysql://{username}:{password}@{host}:{port}/{db}?charset=utf8mb4"
engine = create_async_engine(
        ASYNC_DATABASE_URL,
        echo=True,  # 输出 SQL日志
        pool_size=20,  # 连接池大小
        max_overflow=0,  # 连接池溢出时最大连接数
        pool_recycle=3600,  # 连接池中连接最大空闲时间
        pool_pre_ping=True,  # 检测连接是否可用
        pool_use_lifo=True,  # 使用 LIFO 策略
        future=True,  # 使用异步模式
)

SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)



async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
            await session.close()
        except Exception as e:
            await session.rollback()
            # print(e)
            raise
        finally:
            await session.close()



