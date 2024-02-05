
from aiogram.fsm.state import State, StatesGroup

class CreateInvoice(StatesGroup):
    product = State()
    weight = State()
    size = State()
    addr_from = State()
    addr_to = State()
    way_to_pay = State()

    texts = {
        'CreateInvoice:product' : 'Введите описание груза заново',
        'CreateInvoice:weight' : 'Введите вес груза заново',
        'CreateInvoice:size' : 'Введите габариты груза заново',
        'CreateInvoice:addr_from' : 'Введите адресс отправления груза заново',
        'CreateInvoice:addr_to' : 'Введите адресс получения груза заново',
        'CreateInvoice:way_to_pay' : 'Введите способ оплаты заново',
    }

    
    def __eq__(slc, other):
        return 'CreateInvoice:product' == other


class CreatePretence(StatesGroup):
    id_invoice = State()
    email = State()
    desc = State()
    summa = State()
    photo = State()

    texts = {
        'CreatePretence:id_invoice' : 'Введите номер накладной заново',
        'CreatePretence:email' : 'Введите email заново',
        'CreatePretence:desc' : 'Введите описание ситуации заново',
        'CreatePretence:summa' : 'Введите требуемую сумму заново',
        'CreatePretence:photo' : 'Повторно пришлите фото/скан',
        
    }

    def __eq__(slc, other):
        return 'CreatePretence:id_invoice' == other

