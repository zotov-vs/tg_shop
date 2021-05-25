from aiogram.bot import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline.buttons import forms_inline_keyboard
from keyboards.inline.callback_data import forms_callback
from keyboards.inline.udemy import inline_buttons_1, inline_callback_data_2, inline_callback_data_3
from keyboards.inline.udemy import get_keyboard
from loader import dp

from states.forms import Form
from utils.db_api.models.phones import Phone


@dp.message_handler(text="Проверить номер")
async def start_check_phone(message: types.Message, state: FSMContext):
    await message.answer("Введите номер телефона:")
    await Form.phone.set()


@dp.message_handler(state=Form.phone)
async def answer(message: types.Message, state: FSMContext):
    error_text = await Phone.add(customer_id=message.from_user.id, source_number=message.text)
    if error_text:
        await message.reply(error_text)
    await state.finish()


@dp.message_handler(Command("items"))
async def start_items(message: types.Message):
    await message.answer_photo(photo="https://funik.ru/wp-content/uploads/2018/10/17478da42271207e1d86.jpg",
                               caption="Котик игривый", reply_markup=get_keyboard("100500"))
    await message.answer_photo(photo="https://img3.okidoker.com/c/1/1/3/13297/10277103/22798932_2.jpg",
                               caption="Песики оптом", reply_markup=get_keyboard(100999))


@dp.callback_query_handler(inline_callback_data_2.filter())
async def buying_items(call: CallbackQuery, callback_data: dict):
    item_id = callback_data.get("items_id")
    await call.message.edit_caption(f"Покупай товар номер {item_id}")

@dp.callback_query_handler(inline_callback_data_3.filter(type="like"))
async def buying_like(call: CallbackQuery, callback_data: dict):
    item_id = callback_data.get("items_id")
    await call.answer(f"Тебе понравился этот товар")

@dp.callback_query_handler(inline_callback_data_3.filter(type="dislike"))
async def buying_like(call: CallbackQuery, callback_data: dict):
    item_id = callback_data.get("items_id")
    await call.answer(f" Тебе не понравился этот товар")



# @dp.message_handler(Command("form1"), state=None)
# async def start_form1(message: types.Message, state: FSMContext):
#     await Form1.first()
#     text = await Form1.get_text(state)
#     forms_message = await message.answer(text, reply_markup=forms_inline_keyboard)
#     await state.update_data(
#         {"message_id": forms_message.message_id}
#     )
#
#
# @dp.callback_query_handler(forms_callback.filter(action="previous"))
# async def form1_previous(call: CallbackQuery, callback_data: dict):
#     await call.answer(cache_time=60)
#
#     await Form1.previous()
#     state = dp.current_state(chat=call.message.chat.id, user=call.message.from_user.id)
#     text = await Form1.get_text(state)
#
#     await call.message.answer(text, reply_markup=forms_inline_keyboard)
#
#
# @dp.callback_query_handler(forms_callback.filter(action="next"))
# async def form1_next(call: CallbackQuery, callback_data: dict):
#     await call.answer(cache_time=60)
#
#     await Form1.next()
#     state = dp.current_state(chat=call.message.chat.id, user=call.message.from_user.id)
#     text = await Form1.get_text(state)
#
#     await call.message.answer(text, reply_markup=forms_inline_keyboard)
#
#
# @dp.message_handler(state="*")
# async def answer(message: types.Message, state: FSMContext):
#     text_answer = message.text
#     data = await state.get_data()
#     message_id = data.get("message_id")
#
#     current_state = await state.get_state()
#     error_text = None
#     if (Form1.data.__getitem__(current_state)).check(text_answer):
#         await state.update_data(
#             {f"{current_state}": text_answer}
#         )
#         if current_state != Form1.states_names[-1]:
#             await Form1.next()
#     else:
#         error_text = text_answer
#
#     text = await Form1.get_text(state, error_text=error_text)
#     await message.bot.edit_message_text(text, chat_id=message.chat.id, message_id=message_id
#                                         , reply_markup=forms_inline_keyboard)
#     await message.delete()
