from aiogram import types
from asyncpg import UniqueViolationError
from sqlalchemy import sql, and_

# from data.constants import orders_statuses
from data.localization import currency_symbol
from utils.db_api.database import TimedBaseModel, BaseModel, db

from utils.db_api.models.products import Product


class Order(TimedBaseModel):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customers.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=False)
    discount_percent = db.Column(db.Integer, default=0)

    subtotal = db.Column(db.Integer, default=0)
    customer_discount = db.Column(db.Integer, default=0)
    promocode_discount = db.Column(db.Integer, default=0)
    bonuses = db.Column(db.Integer, default=0)
    noncash = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)

    comment = db.Column(db.String(255), default='')

    query: sql.Select

    async def add_product(self, product: Product, price: int):
        try:
            from utils.db_api.models.orders_lines import OrderLine
            await OrderLine.add(order=self, product=product, price=price, quantity=1)
            await self.recalculate()
            return self
        except UniqueViolationError:
            pass

    async def recalculate(self):
        from utils.db_api.models.orders_lines import OrderLine
        items = await OrderLine.query.where(OrderLine.order_id == self.id).gino.all()
        subtotal = 0
        customer_discount = 0
        promocode_discount = 0
        bonuses = 0
        noncash = 0

        self_update = {}

        for item in items:
            item_update = dict()
            if item.deleted_at:
                if not item.customer_discount == 0:
                    item_update.update({'customer_discount': 0})
                if not item.promocode_discount == 0:
                    item_update.update({'promocode_discount': 0})
                if not item.bonuses == 0:
                    item_update.update({'bonuses': 0})
                if not item.noncash == 0:
                    item_update.update({'noncash': 0})
            else:
                subtotal += item.price * item.quantity
                customer_discount += int(item.price * item.quantity * self.discount_percent / 100)
                if item.customer_discount != int(item.price * self.discount_percent / 100):
                    item_update.update(
                        {'customer_discount': int(item.price * item.quantity * self.discount_percent / 100)})

            if item_update:
                await item.update(**item_update).apply()

        total = subtotal - customer_discount - promocode_discount - bonuses - noncash

        if self.subtotal != subtotal:
            self_update.update({'subtotal': subtotal})
        if self.customer_discount != customer_discount:
            self_update.update({'customer_discount': customer_discount})
        if self.promocode_discount != promocode_discount:
            self_update.update({'promocode_discount': promocode_discount})
        if self.bonuses != bonuses:
            self_update.update({'bonuses': bonuses})
        if self.noncash != noncash:
            self_update.update({'noncash': noncash})
        if self.total != total:
            self_update.update({'total': total})
        if self_update:
            await self.update(**self_update).apply()

    async def get_lines(self, include_deleted=False):
        from utils.db_api.models.orders_lines import OrderLine
        if include_deleted:
            items = await OrderLine.query.where(OrderLine.order_id == self.id).gino.all()
        else:
            items = await OrderLine.query.where(
                and_(OrderLine.order_id == self.id, OrderLine.deleted_at == None)
            ).gino.all()

        return items

    async def set_satus(self, new_status_id: int):
        if new_status_id == 2:
            await self.update(status_id=new_status_id).apply()

    async def get_description(self, need_recalculate: bool = False):

        if need_recalculate:
            await self.recalculate()

        result = f"Заказ №{self.id}\n"
        result += f"-"*50 + "\n\n"
        order_lines = await self.get_lines()

        for line_number, order_line in enumerate(order_lines, 1):
            result += f"{line_number}. " + await order_line.get_description() + "\n"

        result += f"-"*50 + "\n"
        result += "\n"
        if self.subtotal:
            result += f"Сумма товаров: {self.subtotal}{currency_symbol}\n"
        if self.customer_discount:
            result += f"Скидка {self.discount_percent}%: {self.customer_discount}{currency_symbol}\n"
        if self.noncash:
            result += f"Оплачено: {self.noncash}{currency_symbol}\n"
        if self.total:
            result += f"К оплате: {self.total} \n"
        return result

    @classmethod
    async def add(cls, tg_user: types.User):
        try:
            obj = Order(customer_id=tg_user.id, status_id=1)
            await obj.create()
            return obj
        except UniqueViolationError:
            pass

    @classmethod
    async def get_or_add(cls, tg_user: types.User):
        obj = await cls.get(tg_user=tg_user, status_id=1)
        if not obj:
            obj = await cls.add(tg_user=tg_user)
        return obj

    @classmethod
    async def get(cls, order_id: int = None, tg_user: types.User = None, status_id: int = 1):
        if order_id:
            obj = await cls.query.where(
                cls.id == order_id
            ).gino.first()
        else:
            obj = await cls.query.where(
                and_(
                    cls.customer_id == tg_user.id,
                    cls.status_id == status_id
                )
            ).gino.first()

        return obj
