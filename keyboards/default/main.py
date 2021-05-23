from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import data.localization as loc

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(loc.menu_catalog), KeyboardButton(loc.menu_personal_account)],
        [KeyboardButton(loc.menu_help), KeyboardButton(loc.menu_feedback)],
        [KeyboardButton(loc.menu_rules), KeyboardButton(loc.menu_about)],
    ],
    resize_keyboard=True
)
