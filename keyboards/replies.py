from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils import get_notif_string

search_desire = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Девушек'), KeyboardButton(text='Парней')],
    [KeyboardButton(text='Не важно')]
], resize_keyboard=True, one_time_keyboard=True)

searched_by = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Девушкам'), KeyboardButton(text='Парням')],
    [KeyboardButton(text='Не важно')]
], resize_keyboard=True, one_time_keyboard=True)

menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='👤 Моя анкета'), KeyboardButton(text='🚀 Искать анкеты'),
     KeyboardButton(text='❤️ Кто меня оценил?')],
], resize_keyboard=True, one_time_keyboard=True)

profile_keyboard = lambda notif_status: ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='⭐️ Изменить имя'), KeyboardButton(text='🎂 Изменить возраст'),\
     KeyboardButton(text='🚹 Выбрать пол')],
    [KeyboardButton(text='🏙️ Изменить город'), KeyboardButton(text='📄 Изменить описание'),\
      KeyboardButton(text='📷 Изменить фото')],
    [KeyboardButton(text='📝 Заполнить анкету заново'), KeyboardButton(text=get_notif_string(status=notif_status)), KeyboardButton(text='❌ Удалить анкету')],
    [KeyboardButton(text='Назад в меню')]
], resize_keyboard=True, one_time_keyboard=True)