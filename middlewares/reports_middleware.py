import os

from dotenv import load_dotenv
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery
from typing import Callable, Any, Awaitable

from database.requests import get_reports, select_user_profile
from keyboards.inlines import ban

load_dotenv()
ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS').split(',')))


class ReportMiddleware(BaseMiddleware):
    async def __call__(self,
                handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                event: TelegramObject,
                data: dict) -> Any:
        
        result = await handler(event, data)

        if isinstance(event, CallbackQuery) and event.data.startswith('report_user'):
            tg_id = int(event.data.split(':')[1])
            reports_count = await get_reports(tg_id=tg_id)

            if reports_count >= 1:
                bot = data['bot']
                reported_profile = await select_user_profile(tg_id=tg_id)
                
                for admin_id in ADMIN_IDS:
                    await bot.send_photo(
                        chat_id=admin_id,
                        photo=reported_profile.photo,
                        caption=f'{reports_count} жалоб на [\{reported_profile.username}](tg://openmessage?user_id={tg_id}), id \- {tg_id}',
                        parse_mode='MarkdownV2',
                        reply_markup=ban(tg_id=tg_id))
                
        return result