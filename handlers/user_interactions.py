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
        await find_profile(message=message, state=state)
    elif message.text == '❤️ Кто меня оценил?':
        await message.answer('Вас лайкнули:')
    else:
        await message.answer('Нет такого варианта ответа')


@router.message(SearchStates.rate_profile)
async def rate_profile(message: Message, state: FSMContext):
    state_data = await state.get_data()
    liked_profile = state_data['liked_profile']
    liked_id = liked_profile.tg_id
    tg_id = message.from_user.id

    if message.text == '❤️':
        if await requests.insert_like(tg_id=tg_id, liked_id=liked_id, message=None, is_like=True):
            my_profile = await requests.select_user_profile(tg_id=message.from_user.id)
            await requests.set_mutual(tg_id=liked_profile.tg_id, liked_id=my_profile.tg_id)
            await notify_mutual_like(message=message, profile_1=liked_profile, profile_2=my_profile)

        else:
            await find_profile(message=message, state=state)
            await notify_like(message=message, tg_id=liked_id)

    elif message.text == '👎':
        await requests.insert_like(tg_id=tg_id, liked_id=liked_id, message=None, is_like=False)
        await find_profile(message=message, state=state)

    elif message.text == '💌':
        await state.set_state(SearchStates.send_message)
        await message.answer(text='Отправьте пользователю сообщение и он получит его')


@router.message(SearchStates.send_message)
async def send_message(message: Message, state: FSMContext):
    state_data = await state.get_data()
    liked_profile = state_data['liked_profile']
    liked_id = liked_profile.tg_id
    tg_id = message.from_user.id

    if await requests.insert_like(tg_id=tg_id, liked_id=liked_id, message=message.text, is_like=True):
        my_profile = await requests.select_user_profile(tg_id=message.from_user.id)
        await requests.set_mutual(tg_id=liked_profile.tg_id, liked_id=my_profile.tg_id)
        await notify_mutual_like(message=message, profile_1=liked_profile, profile_2=my_profile)
    else:
        await find_profile(message=message, state=state)
        await notify_like(message=message, tg_id=liked_id, has_message=True)


@router.callback_query(F.data == 'watch_likes')
async def watch_likes(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_likes = await requests.get_my_likes(tg_id=callback.from_user.id)

    if not user_likes:
        await callback.message.answer('К сожалению вашу анкету пока никто не лайкнул 😔', reply_markup=kb_i.no_likes)
        return

    for like in user_likes:
        await callback.message.answer_photo(photo=like.user.photo, \
                                            caption=display_like_template(tg_id=like.user.tg_id, username=like.user.username, age=like.user.age,\
                                            sex=like.user.sex, message=like.message, is_mutual=like.is_mutual, city=like.user.city,\
                                            description=like.user.description), reply_markup=kb_i.like_user(like.user.tg_id), parse_mode='MarkdownV2')


@router.callback_query(F.data.startswith('like_user'))
async def like_user(callback: CallbackQuery, state: FSMContext):
    liked_id = int(callback.data.split(':')[1])
    await requests.insert_like(tg_id=callback.from_user.id, liked_id=liked_id)
    # TODO - mutual like


async def notify_like(message: Message, tg_id, has_message=False):
    like_counts = await requests.get_likes_count(tg_id=tg_id)

    if has_message:
        await message.bot.send_message(chat_id=tg_id, text=f'💌 Кто-то отправил вам сообщение!\n\nОбщее количество оценок: {like_counts}', reply_markup=kb_i.watch_likes)
    else:
        await message.bot.send_message(chat_id=tg_id, text=f'❤️ Кто-то оценил вашу анкету!\n\nОбщее количество оценок: {like_counts}', reply_markup=kb_i.watch_likes)


async def notify_mutual_like(message: Message, profile_1, profile_2):
    likes = await requests.get_like_between(profile_1.tg_id, profile_2.tg_id)

    profile_1_tg = await message.bot.get_chat(profile_1.tg_id)
    profile_1_username = profile_1_tg.username
    profile_2_tg = await message.bot.get_chat(profile_2.tg_id)
    profile_2_username = profile_2_tg.username

    messages = [like.message for like in likes if like.message]
    if messages:
        message_1, message_2 = messages
    else:
        message_2 = message_1 = None

    text_1 = display_like_template(
        is_mutual=True,
        tg_id=profile_2.tg_id,
        username=profile_2.username,
        age=profile_2.age,
        city=profile_2.city,
        description=profile_2.description,
        sex=profile_2.sex,
        message=message_2,
        tg_username=profile_2_username,
    )

    await message.bot.send_photo(chat_id=profile_1.tg_id, photo=profile_2.photo, caption=text_1, parse_mode='MarkdownV2')

    text_2 = display_like_template(
        is_mutual=True,
        tg_id=profile_1.tg_id,
        username=profile_1.username,
        age=profile_1.age,
        city=profile_1.city,
        description=profile_1.description,
        sex=profile_1.sex,
        message=message_1,
        tg_username=profile_1_username,
    )

    await message.bot.send_photo(chat_id=profile_2.tg_id, photo=profile_1.photo, caption=text_2, parse_mode='MarkdownV2')


@router.callback_query(F.data == 'resume')
async def continue_watching(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await find_profile(message=callback.message, state=state, user_id=callback.from_user.id)