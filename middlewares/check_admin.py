from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Message
from typing import Callable, Any, Awaitable


class AdminMiddleware(BaseMiddleware):
    def __init__(self, admin_ids: list[int]):
        self.admin_ids = admin_ids
        super().__init__()

    async def __call__(self, handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                event: TelegramObject,
                data: dict) -> Any:
        
        if event.from_user.id in self.admin_ids:
            return await handler(event, data)
        
        if isinstance(event, CallbackQuery):
            await event.message.answer(text='Данная команда доступна только админам')
        elif isinstance(event, Message):
            await event.answer(text='Данная команда доступна только админам')
        
        return