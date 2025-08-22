from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Message
from typing import Callable, Any, Awaitable

from database.requests import is_banned
from messages import BAN


class BanMiddleware(BaseMiddleware):
    async def __call__(self,
                handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                event: TelegramObject,
                data: dict) -> Any:
        
        tg_id = event.from_user.id

        if await is_banned(tg_id=tg_id):
            if isinstance(event, CallbackQuery):
                await event.message.answer(BAN)
                return
            await event.answer(BAN)
            return
        
        return await handler(event, data)