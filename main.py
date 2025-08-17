from aiogram import Bot, Dispatcher
import logging

import asyncio
import os
from dotenv import load_dotenv

from handlers import commands, profile_handlers
from utils import BOT_COMMANDS

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dispatcher = Dispatcher()


async def main():
    dispatcher.include_routers(
        commands.router,
        profile_handlers.router
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