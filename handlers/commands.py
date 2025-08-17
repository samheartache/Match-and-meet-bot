from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import utils
import messages
import keyboards.inlines as kb_i
from keyboards.builders import choice_keyboard

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=utils.welcome_greet(message.from_user.first_name), reply_markup=kb_i.register_button)


@router.message(Command('menu'))
async def menu(message: Message):
    await message.answer(text=messages.MENU_CHOICES, reply_markup=choice_keyboard([i for i in '12345'], size=(3, 2)))


@router.message(Command('editprofile'))
async def edit_profile(message: Message):
    await message.answer(text=messages.EDIT_CHOICES, reply_markup=choice_keyboard([i for i in '1234567'], size=(3, 3)))