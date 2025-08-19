from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

register_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать анкету', callback_data='signup')]
])

watch_likes = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Посмотреть', callback_data='watch_likes'), InlineKeyboardButton(text='Позже', callback_data='watch_later')],
    [InlineKeyboardButton(text='Не уведомлять о лайках', callback_data='notif_off')]
])

like_user = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❤️', callback_data='like_user'), InlineKeyboardButton(text='👎', callback_data='dislike_user')]
])