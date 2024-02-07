from aiogram import types, F, Router
from aiogram.filters import CommandStart

from database.create_db import select_client,  reg_client, find_manager
from keyboards.create_kbd import  keyboard


start_router = Router()

MANADER_ID = None


@start_router.message(CommandStart())
async def start_cmd(message: types.Message):
    isexist = await select_client(message.from_user.id)
    if isexist == 0 :
        await message.answer('Здравствуйте, вы хотите стать нашим клиентом? (ДА/НЕТ)')
        return
    await message.answer('''Здравствуйте, снова рады вас видеть!\nДоступные вам команды:\n/Накладная - создание накладной\n/Претензия - написание претензии\n/Менеджер -  вызов менеджера в чат''', reply_markup=keyboard)
    
@start_router.message((F.text.casefold() == 'да') | (F.text.casefold() == 'нет'))
async def reg_cmd(message: types.Message):
    if message.text.casefold() == 'нет':
        await message.answer('''К сожалению вам не будет доспупен весь функционал.\nЧтобы изменить свое решение, заново пропишите команду /start''')
        return
    global MANADER_ID
    MANADER_ID = await find_manager()
    await reg_client((message.from_user.id, message.from_user.username, MANADER_ID))
    await message.answer(f'''Поздравляем теперь вы наш клиент!\nДоступные вам команды:\n/Накладная - создание накладной\n/Претензия - написание претензии\n/Менеджер -  вызов менеджера в чат''', reply_markup=keyboard)
    