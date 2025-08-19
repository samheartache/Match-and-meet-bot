from sqlalchemy import select, or_, func
from sqlalchemy.orm import joinedload

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
        user_profile = await select_user_profile(tg_id=tg_id)
        user_likes_query = select(Like.liked_id).where(Like.tg_id == tg_id)

        if user_profile.search_desire is not None:
            search_query = select(User).where(
                User.tg_id != user_profile.tg_id,
                User.city == user_profile.city,
                User.age == user_profile.age,
                or_(User.searched_by == user_profile.sex, User.searched_by == None),
                User.sex == user_profile.search_desire,
                User.tg_id.not_in(user_likes_query)
            )
        else:
            search_query = select(User).where(
                User.tg_id != user_profile.tg_id,
                User.city == user_profile.city,
                User.age == user_profile.age,
                or_(User.searched_by == user_profile.sex, User.seached_by == None),
                User.tg_id.not_in(user_likes_query)
            )

        result_profile = await session.scalars(search_query)
        return result_profile.first()


async def insert_like(tg_id, liked_id, message=None, is_like=True):
    async with async_session() as session:
        if has_like(tg_id=tg_id, liked_id=liked_id):
            new_like = Like(
                tg_id=tg_id,
                liked_id=liked_id,
                message=message,
                is_like=is_like,
                is_watched=False,
                is_mutual=True,
            )
        else:
            new_like = Like(
                tg_id=tg_id,
                liked_id=liked_id,
                message=message,
                is_like=is_like,
                is_watched=False,
                is_mutual=False,
            )
        
        session.add(new_like)
        await session.commit()


async def has_like(tg_id, liked_id):
    async with async_session() as session:
        like_query = select(Like).where(Like.tg_id == liked_id, Like.liked_id == tg_id)
        like = await session.scalars(like_query)
        if like:
            return True
        return False


async def get_likes_count(tg_id):
    async with async_session() as session:
        query = select(func.count()).where(Like.liked_id == tg_id)
        result = await session.scalar(query)
        return result or 0


async def get_my_likes(tg_id):
    async with async_session() as session:
        query = (
            select(Like)
            .options(joinedload(Like.user))
            .where(Like.liked_id == tg_id, Like.is_like == True)
        )
        result = await session.scalars(query)
        return result.all()