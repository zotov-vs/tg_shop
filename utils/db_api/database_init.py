import asyncio

from aiogram import Dispatcher

from data.constants import entities_dict, products_types_dict, payments_types_dict
from utils.db_api.models.entities import Entity
from utils.db_api.models.entities_types import EntityType
from utils.db_api.models.statuses import add_status


async def on_startup(dispatcher: Dispatcher):
    for code in entities_dict:
        await Entity.add(code=code, name=entities_dict[code])

    # После того как добавили сущности, добавим их статусы и типы

    entity = await Entity.get(code='product')
    for code in products_types_dict:
        await EntityType.add(code=code, name=products_types_dict[code], entity_id=entity.id)

    entity = await Entity.get(code='payment')
    for code in payments_types_dict:
        await EntityType.add(code=code, name=payments_types_dict[code], entity_id=entity.id)

    # customer's statuses
    for name in ['Администратор', 'Сотрудник', 'Посетитель', 'Подписчик', 'Покупатель', 'VIP',
                 'Черный список', 'Поставщик', 'Спам']:
        await add_status(name)

    # orders status
    for name in ['Новый', 'Ждет оплаты', 'Не подтвержден', 'Оплачен', 'Выполняется', 'Выполнен', 'Новый']:
        await add_status(name)

    # orders products status
    for name in ['Требуется анкета', 'Требуется заявление МНП', 'Выдан', 'Подключение',
                 'Подключен', 'Есть проблемы', 'Возврат']:
        await add_status(name)
