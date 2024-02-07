import os

from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from base.class_fms import CreateInvoice, CreatePretence
from database.create_db import add_invoices, add_pretences, select_manager, select_client,  reg_client, find_manager
from keyboards.create_kbd import builder_pret, keyboard
from create_pdf import simple_table



user_router = Router()

MANADER_ID = None

@user_router.message(CommandStart())
async def start_cmd(message: types.Message):
    isexist = await select_client(message.from_user.id)
    if isexist == 0 :
        await message.answer('Здравствуйте, вы хотите стать нашим клиентом? (ДА/НЕТ)')
        return
    await message.answer('''Здравствуйте, снова рады вас видеть!\nДоступные вам команды:\n/Накладная - создание накладной\n/Претензия - написание претензии\n/Менеджер -  вызов менеджера в чат''', reply_markup=keyboard)
    
@user_router.message((F.text.casefold() == 'да') | (F.text.casefold() == 'нет'))
async def reg_cmd(message: types.Message):
    if message.text.casefold() == 'нет':
        await message.answer('''К сожалению вам не будет доспупен весь функционал.\nЧтобы изменить свое решение, заново пропишите команду /start''')
        return
    global MANADER_ID
    MANADER_ID = await find_manager()
    await reg_client((message.from_user.id, message.from_user.username, MANADER_ID))
    await message.answer(f'''Поздравляем теперь вы наш клиент!\nДоступные вам команды:\n/Накладная - создание накладной\n/Претензия - написание претензии\n/Менеджер -  вызов менеджера в чат''', reply_markup=keyboard)
    


# ----------------------------------Create invoice-----------------------------------
@user_router.message(StateFilter(None), Command('Накладная'))
@user_router.message(StateFilter(None), F.text.casefold() == 'накладная')
async def invoice_cmd(message: types.Message, state:FSMContext):
    await state.update_data(client_id=message.from_user.id)
    await message.answer('Введите описание груза')
    await state.set_state(CreateInvoice.product)

@user_router.message(StateFilter('*'), Command('Отмена'))
@user_router.message(StateFilter('*'), F.text.casefold() == 'отмена')
async def cancle_cmd(message: types.Message, state:FSMContext):
    cur_state = await state.get_data()
    if cur_state is None:
        return
    
    await state.clear()
    await message.answer('Действия отменены')


@user_router.message(StateFilter('*'), Command("назад"))
@user_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def prev_cmd(message: types.Message, state:FSMContext):

    cur_class = CreateInvoice
    cur_state = await state.get_state()

    if cur_state.split(':')[0] == 'CreatePretence':
        cur_class = CreatePretence


    if cur_state == cur_class():
        await message.answer(f'Предыдущего шага нет, если хотите выйти напишите "отмена"')
        return 
    
    prev = None
    for s in cur_class.__all_states__:
        if s.state == cur_state:
            await state.set_state(prev)
            await message.answer(f'Вы вернулись к прошлому шагу \n {cur_class.texts[prev.state]}')
            return
        prev = s
    
    

@user_router.message(CreateInvoice.product, F.text)
async def add_product(message: types.Message, state:FSMContext):
    await state.update_data(product=message.text)
    await message.answer('Введите вес груза')
    await state.set_state(CreateInvoice.weight)

@user_router.message(CreateInvoice.weight, F.text)
async def add_weight(message: types.Message, state:FSMContext):
    await state.update_data(weight=message.text)
    await message.answer('Введите габариты груза')
    await state.set_state(CreateInvoice.size)


@user_router.message(CreateInvoice.size, F.text)
async def add_size(message: types.Message, state:FSMContext):
    await state.update_data(size=message.text)
    await message.answer('Введите адресс отправления')
    await state.set_state(CreateInvoice.addr_from)

@user_router.message(CreateInvoice.addr_from, F.text)
async def add_addr_from(message: types.Message, state:FSMContext):
    await state.update_data(addr_from=message.text)
    await message.answer('Введите адресс получения')
    await state.set_state(CreateInvoice.addr_to)

@user_router.message(CreateInvoice.addr_to, F.text)
async def add_addr_to(message: types.Message, state:FSMContext):
    await state.update_data(addr_to=message.text)
    await message.answer('Введите способ оплаты')
    await state.set_state(CreateInvoice.way_to_pay)

@user_router.message(CreateInvoice.way_to_pay, F.text)
async def add_way_pay(message: types.Message, state:FSMContext):
    await state.update_data(way_to_pay=message.text)
    await message.answer('Накладная успешно создана!!!')
    data = await state.get_data()
    last_id = await add_invoices(data=data)
    simple_table(data, num_inv=last_id[0])
    doc = FSInputFile(f'invoice-{last_id[0]}.pdf')
    await message.answer_document(doc, caption=f'Накладная №{last_id[0]}')
    os.remove(f'invoice-{last_id[0]}.pdf')
    await state.clear()



#---------------------------Create pretence-------------------------

@user_router.message(StateFilter(None), Command('Претензия'))
@user_router.message(StateFilter(None), F.text.casefold() == 'претензия')
async def pretence_cmd(message: types.Message, state:FSMContext):
    await state.update_data(client_id=message.from_user.id)
    await message.answer('Введите номер накладной')
    await state.set_state(CreatePretence.id_invoice)




@user_router.message(CreatePretence.id_invoice, F.text)
async def add_id_product(message: types.Message, state:FSMContext):
    await state.update_data(id_product=int(message.text))
    await message.answer('Введите email для связи')
    await state.set_state(CreatePretence.email)

@user_router.message(CreatePretence.email, F.text)
async def add_email(message: types.Message, state:FSMContext):
    await state.update_data(email=message.text)
    await message.answer('Введите описание ситуации')
    await state.set_state(CreatePretence.desc)

@user_router.message(CreatePretence.desc, F.text)
async def add_desc(message: types.Message, state:FSMContext):
    await state.update_data(desc=message.text)
    await message.answer('Введите требуемую сумму в рублях')
    await state.set_state(CreatePretence.summa)

@user_router.message(CreatePretence.summa, F.text)
async def add_summa(message: types.Message, state:FSMContext):
    await state.update_data(summa=float(message.text))
    await message.answer('Пришлите фото/скан')
    await state.set_state(CreatePretence.photo)

@user_router.message(CreatePretence.photo, F.photo)
async def add_photo(message: types.Message, state:FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer('Готово. Претензия будет доставлена менеждеру.')
    date =  await state.get_data()
    await add_pretences(data=date)
    global MANADER_ID
    if MANADER_ID is None:
        MANADER_ID = await select_manager(message.from_user.id)
    if MANADER_ID is None:
        await message.answer('К сожалению, к вам еще не прикреплен менеджер. Но мы сохранили вашу претензию.')
        return
    await message.bot.send_message(MANADER_ID[0], f"Была создна претензия от пользователя {message.from_user.username} на накладную N{date['id_product']}")  
    await state.clear()

#----------------Call manager-------------------------------


@user_router.message(Command('Менеджер'))
@user_router.message(StateFilter(None), F.text.casefold() == 'менеджер')
async def manager_cmd(message: types.Message):
    global MANADER_ID
    if MANADER_ID is None:
        MANADER_ID = await select_manager(message.from_user.id)
    if MANADER_ID is None:
        await message.answer('К сожалению, к вам еще не прикреплен менеджер.')#заглушка
        return
    await message.bot.send_message(MANADER_ID[0], f'Пользователь {message.from_user.id} вызвал вас в чат {message.date.strftime("%H:%M:%S")}!', reply_markup=builder_pret.as_markup())
    await message.answer('Ваш менеджер скоро войдет в чат')


@user_router.message(F.text)
async def text_cmd(message: types.Message):
    await message.answer('Пожалуйста, используйте команды!!!')
