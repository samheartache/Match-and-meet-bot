from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states import GlobalStates, SearchStates
from handlers.commands import send_myprofile, find_profile, watch_likes, help
from database import requests
import keyboards.inlines as kb_i
from utils import display_like_template
from middlewares.check_ban import BanMiddleware

router = Router()
router.message.middleware(BanMiddleware())
router.callback_query.middleware(BanMiddleware())


@router.message(GlobalStates.menu)
async def menu_choices(message: Message, state: FSMContext):
    if message.text == '👤 Моя анкета':
        await send_myprofile(message=message, state=state)
    elif message.text == '🚀 Искать анкеты':
        await find_profile(message=message, state=state)
    elif message.text == '❤️ Кто меня оценил?':
        await watch_likes(message=message)


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
    
    elif message.text == 'Назад в меню':
        await help(message=message, state=state)


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
async def watch_likes_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await watch_likes(message=callback.message, user_id=callback.from_user.id)


@router.callback_query(F.data.startswith('like_user'))
async def like_user(callback: CallbackQuery, state: FSMContext):
    liked_id = int(callback.data.split(':')[1])
    await callback.answer('')
    await requests.insert_like(tg_id=callback.from_user.id, liked_id=liked_id)
    await notify_mutual_like(message=callback.message, profile_1=await requests.select_user_profile(tg_id=liked_id),\
                              profile_2=await requests.select_user_profile(tg_id=callback.from_user.id))
    await callback.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data.startswith('dislike_user'))
async def like_user(callback: CallbackQuery, state: FSMContext):
    disliked_id = int(callback.data.split(':')[1])
    await callback.answer('')
    await requests.insert_like(tg_id=callback.from_user.id, liked_id=disliked_id, is_like=False)
    await requests.set_watched(tg_id=disliked_id, liked_id=callback.from_user.id)
    await callback.message.edit_reply_markup(reply_markup=None)


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