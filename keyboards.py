from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

register_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать анкету', callback_data='signup')]
])

sex_choice = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Мужской'), KeyboardButton(text='Женский')]
])

search_desire = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Девушек'), KeyboardButton(text='Парней')],
    [KeyboardButton(text='Не важно')]
])