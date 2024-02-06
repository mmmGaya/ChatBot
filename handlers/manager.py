from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from base.class_fms import CreateInvoice, CreatePretence
from database.create_db import add_invoices, add_pretences, reg_client
from keyboards.create_kbd import builder_resp
from aiogram.types import InlineKeyboardButton
from client import user_router



manager_router = Router()



@manager_router.callback_query(F.data == 'callmanager')
async def callbacks_call(callback: types.CallbackQuery):
    client_id = callback.from_user.id
    await callback.bot.send_message(client_id, f"Здравствуйте, {callback.from_user.username}. Чем могу вам помочь?")


