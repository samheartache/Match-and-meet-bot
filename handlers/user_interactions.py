from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states import GlobalStates, SearchStates
from handlers.commands import send_myprofile, find_profile
from database import requests
import keyboards.inlines as kb_i
from utils import display_like_template

router = Router()


@router.message(GlobalStates.menu)
async def menu_choices(message: Message, state: FSMContext):
    if message.text == '👤 Моя анкета':
        await send_myprofile(message=message, state=state)
    elif message.text == '🚀 Искать анкеты':
        print('fjdkfdskjkf')
        await find_profile(message=message, state=state)
    elif message.text == '❤️ Кто меня оценил?':
        await message.answer('Вас лайкнули:')
    else:
        await message.answer('Нет такого варианта ответа')


@router.message(SearchStates.rate_profile)
async def rate_profile(message: Message, state: FSMContext):
    state_data = await state.get_data()
    liked_id = state_data['liked_id']
    tg_id = message.from_user.id

    if message.text == '❤️':
        await requests.insert_like(tg_id=tg_id, liked_id=liked_id, message=None, is_like=True)
        like_counts = await requests.get_likes_count(tg_id=liked_id)
        if like_counts == 1:
            await find_profile(message=message, state=state)
            await message.answer(text='Кто-то оценил вашу анкету!', reply_markup=kb_i.watch_likes)
        elif like_counts % 5 == 0:
            await find_profile(message=message, state=state)
            await message.answer(text=f'У вас уже целых {like_counts} оценок', reply_markup=kb_i.watch_likes)

    elif message.text == '👎':
        await requests.insert_like(tg_id=tg_id, liked_id=liked_id, message=None, is_like=False)
        await find_profile(message=message, state=state)

    elif message.text == '💌':
        await state.set_state(SearchStates.send_message)
        await message.answer(text='Отправьте пользователю сообщение и он получит его')


@router.message(SearchStates.send_message)
async def send_message(message: Message, state: FSMContext):
    state_data = await state.get_data()
    liked_id = state_data['liked_id']
    tg_id = message.from_user.id
    await requests.insert_like(tg_id=tg_id, liked_id=liked_id, message=message.text, is_like=True)
    like_counts = await requests.get_likes_count(tg_id=liked_id)
    if like_counts == 1:
        await find_profile(message=message, state=state)
        await message.bot.send_message(chat_id=liked_id, text='Кто-то оценил вашу анкету!', reply_markup=kb_i.watch_likes)
    elif like_counts % 5 == 0:
        await find_profile(message=message, state=state)
        await message.bot.send_message(chat_id=liked_id, text=f'У вас уже целых {like_counts} оценок', reply_markup=kb_i.watch_likes)


@router.callback_query(F.data == 'watch_likes')
async def watch_likes_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_likes = await requests.get_my_likes(tg_id=712020807)
    for like in user_likes:
        if not like.is_mutual:
            await callback.message.answer_photo(photo=like.user.photo, caption=display_like_template(tg_id=like.user.tg_id, username=like.user.username, age=like.user.age,\
                                                                                                    sex=like.user.sex, message=like.message, is_mutual=like.is_mutual,\
                                                                                                    city=like.user.city, description=like.user.description), reply_markup=kb_i.like_user)
        else:
            await callback.message.answer_photo(photo=like.user.photo, caption=display_like_template(tg_id=like.user.tg_id, username=like.user.username, age=like.user.age,\
                                                                                                    sex=like.user.sex, message=like.message, is_mutual=like.is_mutual,\
                                                                                                    city=like.user.city, description=like.user.description), parse_mode='Markdown')