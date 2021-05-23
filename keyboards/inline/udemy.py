from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

inline_callback_data_1 = CallbackData("inline_buttons_1", "type")

inline_buttons_1 = InlineKeyboardMarkup(row_width=2)
inline_buttons_1.insert(
    InlineKeyboardButton(text="Edit Name", callback_data=inline_callback_data_1.new(type="edit_name")))
inline_buttons_1.insert(
    InlineKeyboardButton(text="Edit Description", callback_data=inline_callback_data_1.new(type="edit_description")))
inline_buttons_1.insert(
    InlineKeyboardButton(text="Edit About", callback_data=inline_callback_data_1.new(type="edit_about")))
inline_buttons_1.insert(
    InlineKeyboardButton(text="Edit Botpic", callback_data=inline_callback_data_1.new(type="edit_botpic")))
inline_buttons_1.insert(
    InlineKeyboardButton(text="Edit Commands", callback_data=inline_callback_data_1.new(type="edit_commands")))
inline_buttons_1.insert(
    InlineKeyboardButton(text="<<Back to Bot", callback_data=inline_callback_data_1.new(type="back_to_bot")))

inline_callback_data_2 = CallbackData("inline_buttons_2", "items_id")
inline_callback_data_3 = CallbackData("inline_buttons_3", "type", "items_id")


def get_keyboard(items_id):
    inline_buttons_3 = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="купить товар"
                                     , callback_data=inline_callback_data_2.new(items_id=f"{items_id}"))
            ],
            [
                InlineKeyboardButton(text="👍"
                                     , callback_data=inline_callback_data_3.new(type="like"
                                                                                , items_id=f"{items_id}")),
                InlineKeyboardButton(text="👎"
                                     , callback_data=inline_callback_data_3.new(type="dislike"
                                                                                , items_id=f"{items_id}"))
            ],
            [
                InlineKeyboardButton(text="Поделиться с другом"
                                     , switch_inline_query=f"{items_id}"),
            ]
        ]
    )

    return inline_buttons_3
