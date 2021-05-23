import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.order import order_ikb, get_order_keyboard, order_edit_ikb, get_edit_keyboard
from loader import dp
from utils.db_api.models.bills import Bill
from utils.db_api.models.orders import Order
from utils.payments import Payment

cache_time = 0


@dp.callback_query_handler(order_ikb.filter(operation="create_bill"))
async def products_list_edit(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=cache_time)
    logging.info(f"call = {callback_data}")

    # Найдем заказ
    order = await Order.get(int(callback_data.get('id')))
    order_text = await order.get_description()

    await order.set_satus(2)

    # 2. Создаем счет на оплату

    bill = await Bill.get_or_add(order=order)
    pay_url = Payment(bill).create()
    if pay_url == 'error':
        pass
    else:
        logging.info(pay_url)
        # 3. Выводим заказ с кнопкой оплаты
        keyboard = await get_order_keyboard(order=order, pay_url=pay_url)
        await call.message.edit_text(order_text, reply_markup=keyboard)


# Редактирование заказа
@dp.callback_query_handler(order_ikb.filter(operation="edit_order"))
async def edit_order(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=cache_time)
    logging.info(f"call = {callback_data}")

    order = await Order.get(int(callback_data.get('id')))
    from utils.db_api.models.orders_lines import OrderLine
    paginator = await OrderLine.paginator(order=order, line_number=1)
    text = await paginator['order_line'].get_description()
    keyboard = await get_edit_keyboard(order_line=paginator['order_line'], page_info=paginator['page'])
    await call.message.edit_text(text, reply_markup=keyboard)


# Возврат из режима редактирования:
@dp.callback_query_handler(order_edit_ikb.filter(operation="edit_order_cancel"))
async def edit_order_cancel(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=cache_time)
    logging.info(f"call = {callback_data}")
    # 2. Выводим заказ для подтверждения
    order = await Order.get(order_id=int(callback_data['order_id']))
    order_text = await order.get_description(True)

    keyboard = await get_order_keyboard(order=order)
    await call.message.edit_text(order_text, reply_markup=keyboard)


# Навигация по строкам заказа
@dp.callback_query_handler(order_edit_ikb.filter(operation="edit_order_navigation"))
async def edit_order_navigation(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=cache_time)
    logging.info(f"call = {callback_data}")

    order = await Order.get(int(callback_data.get('order_id')))
    from utils.db_api.models.orders_lines import OrderLine
    paginator = await OrderLine.paginator(order=order, line_number=int(callback_data.get('page')))
    text = await paginator['order_line'].get_description()
    keyboard = await get_edit_keyboard(order_line=paginator['order_line'], page_info=paginator['page'])
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(order_edit_ikb.filter(operation="edit_order_position"))
async def edit_order_position(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=cache_time, text="номер строки заказа")
    logging.info(f"call = {callback_data}")


@dp.callback_query_handler(order_edit_ikb.filter(operation="edit_order_count"))
async def edit_order_count(call: CallbackQuery, callback_data: dict):
    logging.info(f"call = {callback_data}")
    add_quantity = int(callback_data['add_quantity'])
    if add_quantity == 0:
        await call.answer(cache_time=cache_time, text="количество товара в заказе")
    else:
        await call.answer(cache_time=cache_time)
        order = await Order.get(int(callback_data.get('order_id')))
        from utils.db_api.models.orders_lines import OrderLine
        order_line = await OrderLine.get(int(callback_data.get('id')))
        await order_line.set_quantity(**{'quantity': order_line.quantity + add_quantity})

        paginator = await OrderLine.paginator(order=order, line_number=int(callback_data.get('page')))
        text = await paginator['order_line'].get_description()
        keyboard = await get_edit_keyboard(order_line=paginator['order_line'], page_info=paginator['page'])
        await call.message.edit_text(text, reply_markup=keyboard)



