from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

search_desire = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Девушек'), KeyboardButton(text='Парней')],
    [KeyboardButton(text='Не важно')]
], resize_keyboard=True, one_time_keyboard=True)