from aiogram import Bot, Dispatcher
import logging

import asyncio
import os
from dotenv import load_dotenv

from register_handlers import router

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dispatcher = Dispatcher()


async def main():
    dispatcher.include_router(router=router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot's work was stopped manually")

