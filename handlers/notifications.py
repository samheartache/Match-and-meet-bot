from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from utils import display_like_template
from database import requests
import keyboards.inlines as kb_i

router = Router()


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


@router.callback_query(F.data == 'notif_off')
async def off_notif(callback: CallbackQuery):
    await callback.answer('')
    await requests.set_notif(tg_id=callback.from_user.id, status=False)
    await callback.message.delete()
    await callback.message.answer(text='🔕 Вы отключили уведомления о лайках.\n\nДля включения уведомлений напишите /notif_on')