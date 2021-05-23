import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, InputFile

from keyboards.inline.catalog import catalog_cb

import data.localization as loc
from keyboards.inline.catalog import catalog_cb, get_catalog_keyboard
from keyboards.inline.order import get_order_keyboard
from loader import dp
from states.catalog import Waiting
from states.orders import OrderState
from utils.db_api.models.bills import Bill
from utils.payments import Payment
from utils.db_api.models.products import Product
from utils.db_api.models.orders import Order
from utils.db_api.models.orders_lines import OrderLine
from utils.db_api.models.promocodes import Promocode

cache_time = 1

@dp.message_handler(text=loc.menu_catalog)
async def products_list(message: types.Message):
    product = await Product.get()
    text = await product.get_caption()
    items_list = await product.get_children_list()
    keyboard = await get_catalog_keyboard(product=product, items_list=items_list)
    # photo = product.product_image
    photo = InputFile(f"./data/images/logo.jpg")

    await message.answer_photo(photo, caption=text, reply_markup=keyboard)


@dp.callback_query_handler(catalog_cb.filter(operation="list"))
async def products_list_edit(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=cache_time)
    logging.info(f"call = {callback_data}")

    product = await Product.get(int(callback_data.get('id')))
    text = await product.get_caption()
    items_list = await product.get_children_list()
    keyboard = await get_catalog_keyboard(product=product, items_list=items_list)

    await call.message.edit_caption(caption=text, reply_markup=keyboard)


@dp.callback_query_handler(catalog_cb.filter(operation="back"))
async def products_list_edit(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=cache_time)
    logging.info(f"call = {callback_data}")

    product = await Product.get(int(callback_data.get('parent_id')))
    text = await product.get_caption()
    items_list = await product.get_children_list()
    keyboard = await get_catalog_keyboard(product=product, items_list=items_list)

    await call.message.edit_caption(caption=text, reply_markup=keyboard)


@dp.callback_query_handler(catalog_cb.filter(operation="promocode"))
async def products_list_edit(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=cache_time)
    logging.info(f"call = {callback_data}")
    await call.answer(f"Введите промокод")

    await state.update_data(message_id=call.message.message_id, try_number=0)

    await Waiting.promocode.set()


@dp.message_handler(state=Waiting.promocode)
async def products_list(message: types.Message, state: FSMContext):
    promocode = await Promocode.get(message.text)
    if promocode:
        await message.answer(f"Охренеть")
        await state.reset_state()
    else:
        data = await state.get_data()
        try_number = data.get("try_number")
        try_number += 1

        await state.update_data(try_number=try_number)

        if try_number == 1:
            await message.answer(f"Промокод <code>{message.text.upper()}</code> не найден, проверьте может опечатка?")
        elif try_number == 2:
            await message.answer(f"Такой промокод <code>{message.text.upper()}</code> тоже не найден 😞")
        elif try_number == 3:
            await message.answer(f"И такого <code>{message.text.upper()}</code> тоже нет  😢. "
                                 f"Закрадываются сомнения, что у вас есть промокод 🧐")
        elif try_number == 4:
            await message.answer(f"А вы настойчивы 😉, но с этим кодом <code>{message.text.upper()}</code> тоже неудача 😢")
        else:
            await message.answer(f"Ну все! Я устал! Я ухожу. Такого <code>{message.text.upper()}</code> тоже нет 🤷‍♂️\n"
                                 f"Это была послдняя попытка."
                                 f"Хочешь попытать удачу еще - жми кнопку")

            await state.reset_state()


@dp.callback_query_handler(catalog_cb.filter(operation="add_to_order"))
async def products_list_edit(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=cache_time)
    logging.info(f"call = {callback_data}")

    product = await Product.get(int(callback_data.get('id')))

    # 1. Создаем заказ ли добавим в текущий
    order = await Order.get_or_add(tg_user=call.from_user)
    order = await order.add_product(product=product, price=product.product_price)
    order_text = await order.get_description()

    if OrderState.add_products.state:
        logging.info("Установлено состояние")
    else:
        OrderState.add_products.set()
        logging.info("Не установлено состояние")

    # Получим сообщение с данным заказом
    state_data = await state.get_data()
    orders_message_id = state_data.get('orders_message_id')

    # 2. Выводим заказ для подтверждения
    keyboard = await get_order_keyboard(order=order)
    if orders_message_id:
        await call.bot.delete_message(chat_id=call.message.chat.id, message_id=orders_message_id)

    orders_message = await call.message.answer(order_text, reply_markup=keyboard)

    state_data.update(orders_message_id=orders_message.message_id)
    await state.update_data(data=state_data)




