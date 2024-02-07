from aiogram import Bot, Dispatcher

import asyncio
import os

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from handlers.client import user_router
from handlers.manager import manager_router
from handlers.comein import start_router
from database.create_db import connect_to_database

connect_to_database()
bot = Bot(token=os.getenv('BOT_TOKEN'))    
dp = Dispatcher()


dp.include_router(start_router)
dp.include_router(user_router)
dp.include_router(manager_router)



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=['message, edited_message'])


asyncio.run(main())