from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import operators_callback, forms_callback

operators_list = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="МТС", callback_data=operators_callback.new(operator="mts")),
            InlineKeyboardButton(text="Билайн", callback_data=operators_callback.new(operator="beeline"))
        ],
        [
            InlineKeyboardButton(text="ТЕЛЕ2", callback_data=operators_callback.new(operator="tele2")),
            InlineKeyboardButton(text="Мегафон", callback_data=operators_callback.new(operator="megafon"))
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data="cancel")
        ]
    ]
)

tariffs_mts = InlineKeyboardMarkup(row_width=1)
tariffs_mts.insert(InlineKeyboardButton(text="Smart для своих (безлимит)", callback_data=operators_callback.new(operator="mts")))
tariffs_mts.insert(InlineKeyboardButton(text="Smart для своих (20Гб)", callback_data=operators_callback.new(operator="mts")))
tariffs_mts.insert(InlineKeyboardButton(text="Персональный", callback_data=operators_callback.new(operator="mts")))

forms_inline_keyboard = InlineKeyboardMarkup(row_width=3)
forms_inline_keyboard.insert(InlineKeyboardButton(text="⬅️", callback_data=forms_callback.new(action="previous")))
forms_inline_keyboard.insert(InlineKeyboardButton(text="⬆️ Отправить", callback_data=forms_callback.new(action="finish")))
forms_inline_keyboard.insert(InlineKeyboardButton(text="➡️", callback_data=forms_callback.new(action="next")))


