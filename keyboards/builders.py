from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

def choice_keyboard(choices: str | list[str], size: tuple[int]=(1, 1)) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    if isinstance(choices, str):
        choices = [choices]
    
    [builder.button(text=choice) for choice in choices]
    x, y = size
    builder.adjust(*[x] * y)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)