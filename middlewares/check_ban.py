from aiogram import BaseMiddleware
from aiogram.types import Message

from database.requests import select_user_profile


class BanMiddleware(BaseMiddleware):
    async def __call__(self, handler, message: Message, data: dict):
        tg_id = message.from_user.id

        user_profile = await select_user_profile(tg_id=tg_id)
        if user_profile.is_banned:
            await message.answer('❗ Вы были забанены в боте.\nПохоже, что на вас было оставлено много жалоб.\nДля выяснения обстоятельств оброщайтесь в поддержку - "@поддержка"')
            return
        return await handler(message, data)