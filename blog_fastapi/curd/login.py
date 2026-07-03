from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User

async def login(db: AsyncSession, username: str, password: str):
    return None

async def register(db: AsyncSession, user: User):
    return None