from aiogram import Bot, Dispatcher
import logging

import asyncio
import os
from dotenv import load_dotenv

from handlers import commands, edit, register, user_interactions
from utils import BOT_COMMANDS
from database.config import start_db_engine

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dispatcher = Dispatcher()


async def main():
    await start_db_engine()
    dispatcher.include_routers(
        commands.router,
        register.router,
        edit.router,
        user_interactions.router,
    )
    await bot.set_my_commands(BOT_COMMANDS)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot's work was stopped manually")