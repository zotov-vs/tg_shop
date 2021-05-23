# https://habr.com/ru/post/129201/
from utils.db_api.models.entities import Entity
from utils.db_api.models.entities_types import EntityType

import asyncio


class Dict(dict):
    def __new__(cls, *args, **kwargs) -> object:
        self = dict.__new__(cls, *args, **kwargs)
        self.__dict__ = self
        return self

entities_dict = {'customer': 'Справочник пользователей',
                 'product': 'Справочник товоров и услуг',
                 'promocode': 'Справочник промокодов',
                 'order': 'Заказы пользователя',
                 'order_line': 'Строка заказа',
                 'payment': 'история платежей'}

products_types_dict = {'folder': 'Папка',
                       'service': 'Услуга',
                       'product': 'Товар (физическая поставка)',
                       'virtual': 'Товар (электронная поставка)'}

payments_types_dict = {'noncash_top_up': 'Пополнение баланса',
                       'noncash_to_order': 'Списание в заказ',
                       'noncash_from_order': 'Возврат из заказа',
                       'noncash_return': 'Возврат с баланса'}

# async def create_dict(entity_id: int = 0):
#     if entity_id == 0:
#         objs = await Entity.get_all()
#         result = Dict(**{obj.code: obj.id for obj in objs})
#     else:
#         objs = await EntityType.get_all(entity_id=entity_id)
#         result = Dict(**{obj.code: obj.id for obj in objs})
#     return result
#
#
# loop = asyncio.get_event_loop()
# entities = loop.run_until_complete(create_dict())
# products_types = loop.run_until_complete(create_dict(entities.product))
# payments_types = loop.run_until_complete(create_dict(entities.payment))
# orders_statuses = loop.run_until_complete(create_dict(entities.payment))
# loop.close()
