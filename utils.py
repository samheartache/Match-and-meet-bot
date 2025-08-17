from aiogram.types import BotCommand

BOT_COMMANDS = [
    BotCommand(command='start', description='Регистрация'),
    BotCommand(command='profile', description='Моя анкета'),
    BotCommand(command='editprofile', description='Редактировать анкету'),
    BotCommand(command='search', description='Искать анкеты'),
    BotCommand(command='likes', description='Кто меня оценил?'),
    BotCommand(command='contacts', description='Контакты бота'),
    BotCommand(command='deleteprofile', description='Удалить анкету'),
]


def welcome_greet(name):
    return f'Привет, {name}. \nДобро пожаловать в бот для знакомтсв. \nДля того чтобы пользоваться ботом, необходимо создать свою анкету.'

def formatted_commands():
    commands = ''
    for c in BOT_COMMANDS:
        commands += f'/{c.command} - {c.description}\n'
    return commands