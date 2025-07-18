from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import utils
import keyboards.inlines as kb_i

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=utils.welcome_greet(message.from_user.first_name), reply_markup=kb_i.register_button)