from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import utils
import messages
import keyboards.inlines as kb_i
from keyboards.replies import menu_keyboard
from states import GlobalStates

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=utils.welcome_greet(message.from_user.first_name), reply_markup=kb_i.register_button)


@router.message(Command('help'))
async def help(message: Message, state: FSMContext):
    await state.set_state(GlobalStates.menu)
    await message.answer(text=messages.HELP, reply_markup=menu_keyboard)