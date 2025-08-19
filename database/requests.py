from sqlalchemy import select

from database.models import User, Like
from database.config import async_session


async def insert_user(user_data, tg_id):
    async with async_session() as session:
        query = select(User).where(User.tg_id == tg_id)
        user = await session.scalar(query)

        if not user:
            new_user = User(**user_data)
            session.add(new_user)
        else:
            for property in user_data.keys():
                setattr(user, property, user_data[property])
        
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


async def find_profile(tg_id):
    async with async_session() as session:
        print('jdkssljdksljklfjdksl')
        input()
        user_profile = await select_user_profile(tg_id=tg_id)
        user_likes_query = select(Like.liked_id).where(Like.tg_id == tg_id)
        search_query = select(User).where(
            User.tg_id != user_profile.tg_id,
            User.city == user_profile.city,
            User.age == user_profile.age,
            User.searched_by == user_profile.sex,
            User.sex == user_profile.search_desire,
            User.tg_id.not_in(user_likes_query)
        )

        result_profile = await session.scalars(search_query)
        return result_profile.first()

