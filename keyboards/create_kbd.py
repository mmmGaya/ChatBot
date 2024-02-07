from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

kb = [
    [
        KeyboardButton(text='/Накладная'),
        KeyboardButton(text='/Претензия'),
        KeyboardButton(text='/Менеджер'),

    ],
]

keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Доступные действия"
    )


builder_pret = InlineKeyboardBuilder()
builder_pret.add(InlineKeyboardButton(text='Ответить', callback_data='callmanager'))




