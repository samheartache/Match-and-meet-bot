from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import utils
import messages
import keyboards.inlines as kb_i
from keyboards.replies import menu_keyboard
from states import GlobalStates, SearchStates
import keyboards.replies as kb_r
from keyboards.builders import choice_keyboard
from database import requests
from utils import display_like_template, userprofile_template, foundprofile_template
from middlewares.check_ban import BanMiddleware

router = Router()
router.message.middleware(BanMiddleware())
router.callback_query.middleware(BanMiddleware())


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=utils.welcome_greet(message.from_user.first_name), reply_markup=kb_i.register_button)


@router.message(Command('help'))
async def help(message: Message, state: FSMContext):
    await state.set_state(GlobalStates.menu)
    await message.answer(text=messages.HELP, reply_markup=menu_keyboard)


@router.message(Command('profile'))
async def send_myprofile(message: Message, state: FSMContext, after_register=False):
    await state.set_state(GlobalStates.profile_edit)
    await message.answer('Вот ваша анкета: ')
    user = await requests.select_user_profile(tg_id=message.from_user.id)
    if not after_register:
        await message.answer_photo(
        photo=user.photo, caption=userprofile_template(username=user.username, age=user.age, city=user.city,\
        description=user.description, sex=user.sex, search_desire=user.search_desire, searched_by=user.searched_by)
        , reply_markup=kb_r.profile_keyboard(notif_status=user.notifications))
    else:
        await message.answer_photo(
            photo=user.photo, caption=userprofile_template(username=user.username, age=user.age, city=user.city,\
            description=user.description, sex=user.sex, search_desire=user.search_desire, searched_by=user.searched_by)
            )


@router.message(Command('search'))
async def find_profile(message: Message, state: FSMContext, user_id=None):
    tg_id = user_id if user_id else message.from_user.id

    found_profile = await requests.find_profile(tg_id=tg_id)
    if found_profile:
        await message.answer_photo(photo=found_profile.photo, caption=foundprofile_template(username=found_profile.username, age=found_profile.age,\
                                                                                            city=found_profile.city, description=found_profile.description, sex=found_profile.sex),\
                                                                                            reply_markup=choice_keyboard(['❤️', '👎', '💌', 'Назад в меню'], size=(3, 1)))
        await state.update_data(liked_profile=found_profile)
        await state.set_state(SearchStates.rate_profile)


@router.message(Command('likes'))
async def watch_likes(message: Message, user_id=None):
    tg_id = user_id if user_id else message.from_user.id
    user_likes = await requests.get_my_likes(tg_id=tg_id)

    if not user_likes:
        await message.answer('К сожалению вашу анкету пока никто не лайкнул 😔', reply_markup=kb_i.no_likes)
        return

    for like in user_likes:
        await message.answer_photo(photo=like.user.photo, \
                                            caption=display_like_template(tg_id=like.user.tg_id, username=like.user.username, age=like.user.age,\
                                            sex=like.user.sex, message=like.message, is_mutual=like.is_mutual, city=like.user.city,\
                                            description=like.user.description), reply_markup=kb_i.like_user(like.user.tg_id), parse_mode='MarkdownV2')


@router.message(Command('notif_on'))
async def notif_on(message: Message):
    await requests.set_notif(tg_id=message.from_user.id, status=True)
    await message.answer(text='🔔 Вы включили уведомления о лайках', reply_markup=kb_r.profile_keyboard(notif_status=True))


@router.message(Command('notif_off'))
async def notif_off(message: Message):
    await requests.set_notif(tg_id=message.from_user.id, status=False)
    await message.answer(text='🔕 Вы отключили уведомления о лайках.\n\nДля включения уведомлений напишите /notif_on', reply_markup=kb_r.profile_keyboard(notif_status=False))