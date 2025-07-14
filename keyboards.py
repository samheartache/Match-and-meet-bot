from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

register_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать анкету', callback_data='signup_button')]
])