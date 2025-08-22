from sqlalchemy import select, or_, func, desc
from sqlalchemy.orm import joinedload, aliased

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

        LikeAlias = aliased(Like)

        if user_profile.search_desire:
            search_query = (
                select(User)
                .outerjoin(
                    LikeAlias,
                    (LikeAlias.liked_id == User.tg_id) & (LikeAlias.tg_id == tg_id)
                )
                .where(
                    User.tg_id != user_profile.tg_id,
                    User.city == user_profile.city,
                    User.age == user_profile.age,
                    or_(User.searched_by == user_profile.sex, User.searched_by == None),
                    User.sex == user_profile.search_desire,
                )
                .order_by(LikeAlias.time_created.isnot(None), LikeAlias.time_created.asc())
            )
        else:
            search_query = (
                select(User)
                .outerjoin(
                    LikeAlias,
                    (LikeAlias.liked_id == User.tg_id) & (LikeAlias.tg_id == tg_id)
                )
                .where(
                    User.tg_id != user_profile.tg_id,
                    User.city == user_profile.city,
                    User.age == user_profile.age,
                    or_(User.searched_by == user_profile.sex, User.searched_by == None),
                )
                .order_by(LikeAlias.time_created.isnot(None), LikeAlias.time_created.asc())
            )

        result = await session.scalars(search_query)
        return result.first()


async def insert_like(tg_id, liked_id, message=None, is_like=True):
    async with async_session() as session:
        new_like = Like(
            tg_id=tg_id,
            liked_id=liked_id,
            message=message,
            is_like=is_like
        )

        if await has_like(tg_id=tg_id, liked_id=liked_id):
            if is_like:
                new_like.is_watched = True
                new_like.is_mutual = True
            else:
                new_like.is_watched = None
                new_like.is_mutual = False
        else:
            if is_like:
                new_like.is_watched = False
                new_like.is_mutual = False
            else:
                new_like.is_watched = None
                new_like.is_mutual = False
        
        session.add(new_like)
        is_mutual = new_like.is_mutual

        await session.commit()

        return is_mutual


async def has_like(tg_id, liked_id):
    async with async_session() as session:
        like_query = select(Like).where(Like.tg_id == liked_id, Like.liked_id == tg_id, Like.is_mutual == False, Like.is_watched == False)
        result = await session.scalars(like_query)
        return result.first() is not None


async def get_likes_count(tg_id):
    async with async_session() as session:
        query = select(func.count()).where(Like.liked_id == tg_id, Like.is_mutual == False, Like.is_like == True)
        result = await session.scalar(query)
        return result or 0


async def get_my_likes(tg_id):
    async with async_session() as session:
        query = (
            select(Like)
            .options(joinedload(Like.user))
            .where(Like.liked_id == tg_id, Like.is_like == True, Like.is_watched == False, Like.is_mutual == False)
        )
        result = await session.scalars(query)
        return result.all()


async def get_like_between(user_id_1, user_id_2):
    async with async_session() as session:
        query = (
            select(Like)
            .where(
                ((Like.tg_id == user_id_1) & (Like.liked_id == user_id_2))
                | ((Like.tg_id == user_id_2) & (Like.liked_id == user_id_1))
            )
            .order_by(desc(Like.time_created))
        )
        result = await session.scalars(query)
        likes = result.all()

    latest_from_user1 = next((like for like in likes if like.tg_id == user_id_1), None)
    latest_from_user2 = next((like for like in likes if like.tg_id == user_id_2), None)

    return latest_from_user1, latest_from_user2


async def set_mutual(tg_id, liked_id):
    async with async_session() as session:
        query = select(Like).where(Like.tg_id == tg_id, Like.liked_id == liked_id, Like.is_mutual == False)
        like = await session.scalar(query)
        like.is_mutual = True
        like.is_watched = True

        await session.commit()


async def add_report(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.reports_count += 1
        await session.commit()


async def get_reports(tg_id):
    async with async_session() as session:
        user_reports = await session.scalar(select(User.reports_count).where(User.tg_id == tg_id))
        return user_reports or 0


async def ban_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.is_banned = True
        await session.commit()
