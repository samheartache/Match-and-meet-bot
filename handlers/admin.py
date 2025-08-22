import re
import os

from dotenv import load_dotenv
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from middlewares.check_admin import AdminMiddleware
from database.requests import set_ban, select_user_profile
from keyboards.inlines import unban, ban
from utils import CMD_REGEXP
from messages import UNBAN, BAN

load_dotenv()
ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS').split(',')))

router = Router()
router.message.middleware(AdminMiddleware(ADMIN_IDS))
router.callback_query.middleware(AdminMiddleware(ADMIN_IDS))


@router.callback_query(F.data.startswith('ban_user'))
async def ban_user(callback: CallbackQuery):
    banned_id = int(callback.data.split(':')[1])
    await set_ban(tg_id=banned_id, status=True)
    await callback.answer('Пользователь был забанен')
    await callback.message.answer('Пользователь был забанен')
    await callback.bot.send_message(chat_id=banned_id, text=BAN)
    await callback.message.edit_reply_markup(reply_markup=unban(tg_id=banned_id))


@router.message(F.text.startswith('/ban'))
async def ban_command(message: Message):
    if re.fullmatch(CMD_REGEXP, message.text):
        banned_id = int(message.text.split()[1])
        profile = await select_user_profile(tg_id=banned_id)
        if profile:
            await set_ban(tg_id=banned_id, status=True)
            await message.answer_photo(photo=profile.photo, caption=f'Пользователь [\{profile.username}](tg://openmessage?user_id={banned_id}) был забанен', parse_mode='MarkdownV2')
            await message.bot.send_message(chat_id=banned_id, text=BAN)
            return
        await message.answer('Пользователь с таким id не найден')


@router.callback_query(F.data.startswith('unban_user'))
async def unban_user(callback: CallbackQuery):
    unbanned_id = int(callback.data.split(':')[1])
    await set_ban(tg_id=unbanned_id, status=False)
    await callback.answer('Пользователь был разбанен')
    await callback.message.answer('Пользователь был разбанен')
    await callback.bot.send_message(chat_id=unbanned_id, text=UNBAN)
    await callback.message.edit_reply_markup(reply_markup=ban(tg_id=unbanned_id))



@router.message(F.text.startswith('/rban'))
async def rban_command(message: Message):
    if re.fullmatch(CMD_REGEXP, message.text):
        unbanned_id = int(message.text.split()[1])
        profile = await select_user_profile(tg_id=unbanned_id)
        if profile:
            await set_ban(tg_id=unbanned_id, status=False)
            await message.answer_photo(photo=profile.photo, caption=f'Пользователь [\{profile.username}](tg://openmessage?user_id={unbanned_id}) был разбанен', parse_mode='MarkdownV2')
            await message.bot.send_message(chat_id=unbanned_id, text=UNBAN)
            return
        await message.answer('Пользователь с таким id не найден')  