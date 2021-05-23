from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.localization import menu_cancel, currency_symbol
from utils.db_api.models.entities_types import EntityType
from utils.db_api.models.products import Product

catalog_cb = CallbackData('catalog', 'operation', 'id', 'parent_id', 'entity_type_id')


async def get_catalog_keyboard(product: Product, items_list: list, admin_mode=False):
    keyboard = InlineKeyboardMarkup(row_width=1)
    entity = await EntityType.get(code='folder')
    if product.entity_type_id == entity.id:
        for item in items_list:
            keyboard.insert(
                InlineKeyboardButton(text=f"{item.product_name}",
                                     callback_data=catalog_cb.new(operation='list',
                                                                  id=item.id,
                                                                  parent_id=item.parent_id,
                                                                  entity_type_id=item.entity_type_id
                                                                  )

                                     ))
    else:
        keyboard.insert(
            InlineKeyboardButton(text=f"Купить {product.product_price} {currency_symbol}",
                                 callback_data=catalog_cb.new(operation='add_to_order',
                                                              id=product.id,
                                                              parent_id=product.parent_id,
                                                              entity_type_id=product.entity_type_id
                                                              )))
        keyboard.insert(
            InlineKeyboardButton(text=f"У меня есть промокод 🏷",
                                 callback_data=catalog_cb.new(operation='promocode',
                                                              id=product.id,
                                                              parent_id=product.parent_id,
                                                              entity_type_id=product.entity_type_id
                                                              )))


    if product.id:
        keyboard.insert(
            InlineKeyboardButton(text=menu_cancel,
                                 callback_data=catalog_cb.new(operation='back',
                                                              id=product.id,
                                                              parent_id=product.parent_id,
                                                              entity_type_id=product.entity_type_id
                                                              )
                                 )
        )

    return keyboard
