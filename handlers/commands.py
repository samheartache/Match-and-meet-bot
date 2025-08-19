from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import utils
import messages
import keyboards.inlines as kb_i
from keyboards.replies import menu_keyboard
from states import GlobalStates
import keyboards.replies as kb_r
from database import requests
from utils import userprofile_template

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=utils.welcome_greet(message.from_user.first_name), reply_markup=kb_i.register_button)


@router.message(Command('help'))
async def help(message: Message, state: FSMContext):
    await state.set_state(GlobalStates.menu)
    await message.answer(text=messages.HELP, reply_markup=menu_keyboard)


@router.message(Command("profile"))
async def send_profile(message: Message, state: FSMContext, after_register=False):
    await state.set_state(GlobalStates.profile_edit)
    await message.answer('Вот ваша анкета: ')
    user = await requests.select_user_profile(tg_id=message.from_user.id)
    if not after_register:
        if user.description:
            await message.answer_photo(
            photo=user.photo, caption=userprofile_template(username=user.username, age=user.age, city=user.city,\
            description=user.description, sex=user.sex, search_desire=user.search_desire, searched_by=user.searched_by)
            , reply_markup=kb_r.profile_keyboard)
    else:
        await message.answer_photo(
            photo=user.photo, caption=userprofile_template(username=user.username, age=user.age, city=user.city,\
            description=user.description, sex=user.sex, search_desire=user.search_desire, searched_by=user.searched_by)
            )