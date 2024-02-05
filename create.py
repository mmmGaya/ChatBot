from aiogram import Bot, Dispatcher, types
from aiogram.fsm.strategy import FSMStrategy
import asyncio
import os

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from handlers.client import user_router
from base.command_list import command_user_list

bot = Bot(token=os.getenv('BOT_TOKEN'))    
dp = Dispatcher()

dp.include_router(user_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.set_my_commands(commands=command_user_list, scope=types.BotCommandScopeAllPrivateChats())
    # await bot.set_my_commands(command_user_list)

    await dp.start_polling(bot, allowed_updates=['message, edited_message'])








asyncio.run(main())