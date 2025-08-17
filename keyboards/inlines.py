from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

register_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать анкету', callback_data='signup')]
])