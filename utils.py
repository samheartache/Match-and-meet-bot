from aiogram.types import BotCommand

BOT_COMMANDS = [
    BotCommand(command='start', description='Регистрация'),
    BotCommand(command='help', description='Список команд'),
    BotCommand(command='profile', description='Моя анкета'),
    BotCommand(command='search', description='Искать анкеты'),
    BotCommand(command='likes', description='Кто меня оценил?'),
    BotCommand(command='contacts', description='Контакты бота'),
    BotCommand(command='deleteprofile', description='Удалить анкету'),
]

SEX = {0: 'Женский', 1: 'Мужской'}
SEARCH_DESIRE = {0: 'Девушек', 1: 'Парней', None: 'Всех'}
SEARCHED_BY = {0: 'Девушкам', 1: 'Парням', None: 'Всем'}
SEX_EMOJI = {0: '👩🏻', 1: '🧑🏻', None: '🚻'}


def welcome_greet(name):
    return f'Привет, {name}. \nДобро пожаловать в бот для знакомтсв. \nДля того чтобы пользоваться ботом, необходимо создать свою анкету.'

def formatted_commands():
    commands = ''
    for c in BOT_COMMANDS:
        commands += f'/{c.command} - {c.description}\n'
    return commands

def userprofile_template(username, age, city, description, sex, search_desire, searched_by):
    if description:
        return f'⭐ Имя: {username}\n🎂 Возраст: {age}\n🏙️ Город: {city}\n📝 Описание: {description}\n\nВаш пол: {SEX_EMOJI[sex]} {SEX[sex]}\nХотите искать: {SEX_EMOJI[search_desire]} {SEARCH_DESIRE[search_desire]}\nВаша анкета видна: {SEX_EMOJI[searched_by]} {SEARCHED_BY[searched_by]}'
    else:
        return f'⭐ Имя: {username}\n🎂 Возраст: {age}\n🏙️ Город: {city}\n\nВаш пол: {SEX_EMOJI[sex]} {SEX[sex]}\nХотите искать: {SEX_EMOJI[search_desire]} {SEARCH_DESIRE[search_desire]}\nВаша анкета видна: {SEX_EMOJI[searched_by]} {SEARCHED_BY[searched_by]}'


def foundprofile_template(username, age, city, description, sex):
    if description:
        return f'{SEX_EMOJI[sex]}: {username}, {age} \n📝: {description}\n🏙️: {city}'
    else:
        return f'{SEX_EMOJI[sex]}: {username}, {age}\n🏙️: {city}'


def display_like_template(tg_id, username, age, city, description, sex, message=None, is_mutual=False):
    if is_mutual:
        result = f'У вас взаимный лайк с [{username}](tg://user?id={tg_id})\n\n{SEX_EMOJI[sex]}: {username}, {age} \n📝: {description}\n🏙️: {city}'
    else:
        result = f'Вас лайкнул {username}\n{SEX_EMOJI[sex]}: {username}, {age} \n📝: {description}\n🏙️: {city}'
    if message:
        result += f'\nСообщение для вас:\n{message}'
    return result