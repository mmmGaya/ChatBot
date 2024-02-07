from aiogram import types, Router, F


manager_router = Router()

@manager_router.callback_query(F.data == 'callmanager')
async def callbacks_call(callback: types.CallbackQuery):
    client_id = callback.from_user.id
    await callback.bot.send_message(client_id, f"Здравствуйте, {callback.from_user.username}. Чем могу вам помочь?")


