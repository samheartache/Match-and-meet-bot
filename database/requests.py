from sqlalchemy import select

from database.models import User, Like
from database.config import async_session


async def insert_user(user_data):
    async with async_session() as session:
        user = User(**user_data)
        session.add(user)
        await session.commit()


async def select_user_profile(tg_id):
    async with async_session() as session:
        query = select(User).where(User.tg_id == tg_id)
        result = await session.scalars(query)
        return result.first()
    

async def update_single_property(tg_id, property, new_value):
    async with async_session() as session:
        query = select(User).where(User.tg_id == tg_id)
        user = await session.scalar(query)
        setattr(user, property, new_value)
        await session.commit()