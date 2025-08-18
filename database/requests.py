from sqlalchemy import select

from database.models import User, Like
from database.config import async_session

# async def insert_user(user_data):