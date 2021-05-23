from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api.models.orders import Order

from data.localization import emoji_yes, emoji_no, emoji_card, currency_symbol, emoji_refresh, emoji_edit, emoji_minus, \
    emoji_plus, menu_add_to_cart, menu_remove_from_cart, menu_next, menu_previous, menu_cancel
from utils.db_api.models.orders_lines import OrderLine

order_ikb = CallbackData('order', 'operation', 'id', 'status_id', 'sum')

order_edit_ikb = CallbackData('order_edit', 'operation', 'id', 'order_id', 'product_id', 'add_quantity', 'page')


async def get_order_keyboard(order: Order, pay_url: str = ""):

    keyboard = InlineKeyboardMarkup(row_width=1)
    if order.status_id == 1:
        keyboard.insert(
            InlineKeyboardButton(text=f"{emoji_edit} Редактировать заказ",
                                 callback_data=order_ikb.new(operation='edit_order',
                                                             id=order.id,
                                                             status_id=order.status_id,
                                                             sum=order.total)
                                 ))
        keyboard.insert(
            InlineKeyboardButton(text=f"{emoji_card} Оплатить Card или Qiwi",
                                 callback_data=order_ikb.new(operation='create_bill',
                                                             id=order.id,
                                                             status_id=order.status_id,
                                                             sum=order.total)
                                 ))
        keyboard.insert(
            InlineKeyboardButton(text=f"{emoji_no} Отменить заказ",
                                 callback_data=order_ikb.new(operation='no_confirm',
                                                             id=order.id,
                                                             status_id=order.status_id,
                                                             sum=order.total)
                                 ))
    if order.status_id == 2:
        keyboard.insert(
            InlineKeyboardButton(text=f"{emoji_card} Перейти к оплате",
                                 url=f"{pay_url}"
                                 ))
        keyboard.insert(
            InlineKeyboardButton(text=f"{emoji_refresh} Проверить оплату",
                                 callback_data=order_ikb.new(operation='check_pay',
                                                             id=order.id,
                                                             status_id=order.status_id,
                                                             sum=order.total)
                                 ))
        keyboard.insert(
            InlineKeyboardButton(text=f"{emoji_no} Отменить заказ",
                                 callback_data=order_ikb.new(operation='no_confirm',
                                                             id=order.id,
                                                             status_id=order.status_id,
                                                             sum=order.total)
                                 ))
    return keyboard


async def get_edit_keyboard(order_line: OrderLine, page_info: dict):
    keyboard = InlineKeyboardMarkup(row_width=1)
    #   -   | 1 шт  |   +
    #  << | < | 2 / 4 | > | >>
    #       << Назад
    # 'order_edit', 'operation', 'id', 'order_id', 'product_id', 'add_quantity', 'page'
    keyboard.row(
        InlineKeyboardButton(text=f"{menu_remove_from_cart}",
                             callback_data=order_edit_ikb.new(operation='edit_order_count',
                                                              id=order_line.id,
                                                              order_id=order_line.order_id,
                                                              product_id=order_line.product_id,
                                                              add_quantity=-1,
                                                              page=page_info['current'],
                                                              )
                             ),
        InlineKeyboardButton(text=f"{order_line.quantity} шт",
                             callback_data=order_edit_ikb.new(operation='edit_order_count',
                                                              id=order_line.id,
                                                              order_id=order_line.order_id,
                                                              product_id=order_line.product_id,
                                                              add_quantity=0,
                                                              page=page_info['current'],)
                             ),
        InlineKeyboardButton(text=f"{menu_add_to_cart}",
                             callback_data=order_edit_ikb.new(operation='edit_order_count',
                                                              id=order_line.id,
                                                              order_id=order_line.order_id,
                                                              product_id=order_line.product_id,
                                                              add_quantity=1,
                                                              page=page_info['current'],)
                             )
    )

    keyboard.row(
        InlineKeyboardButton(text=f"{menu_previous}",
                             callback_data=order_edit_ikb.new(operation='edit_order_navigation',
                                                              id=order_line.id,
                                                              order_id=order_line.order_id,
                                                              product_id=order_line.product_id,
                                                              add_quantity=0,
                                                              page=page_info['previous'],)
                             ),
        InlineKeyboardButton(text=f"{page_info['current']} из {page_info['last']}",
                             callback_data=order_edit_ikb.new(operation='edit_order_position',
                                                              id=order_line.id,
                                                              order_id=order_line.order_id,
                                                              product_id=order_line.product_id,
                                                              add_quantity=0,
                                                              page=page_info['next'])
                             ),
        InlineKeyboardButton(text=f"{menu_next}",
                             callback_data=order_edit_ikb.new(operation='edit_order_navigation',
                                                              id=order_line.id,
                                                              order_id=order_line.order_id,
                                                              product_id=order_line.product_id,
                                                              add_quantity=0,
                                                              page=page_info['next'])
                             )
    )
    keyboard.add(
        InlineKeyboardButton(text=f"{menu_cancel}",
                             callback_data=order_edit_ikb.new(operation='edit_order_cancel',
                                                              id=order_line.id,
                                                              order_id=order_line.order_id,
                                                              product_id=order_line.product_id,
                                                              add_quantity=0,
                                                              page=page_info['next']))
                             )

    return keyboard
