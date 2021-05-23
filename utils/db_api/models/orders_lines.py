import logging

from asyncpg import UniqueViolationError
from sqlalchemy import sql, and_, func

from data.localization import currency_symbol, emoji_delete
from utils.db_api.database import TimedBaseModel, BaseModel, db
from utils.db_api.models.orders import Order
from utils.db_api.models.products import Product


class OrderLine(TimedBaseModel):
    __tablename__ = 'orders_lines'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    customer_discount = db.Column(db.Integer, default=0)
    promocode_id = db.Column(db.Integer, db.ForeignKey('promocodes.id'), nullable=True)
    promocode_discount = db.Column(db.Integer, default=0)
    bonuses = db.Column(db.Integer, default=0)
    noncash = db.Column(db.Integer, default=0)

    query: sql.Select

    @property
    async def product(self):
        item = await Product.get(self.product_id)
        return item

    async def get_description(self):
        product = await self.product
        result = f""
        if self.deleted_at is not None:
            result = f"{emoji_delete} строка удалена\n"
        result += f"{product.product_name}\n" \
                  f"<code>{self.quantity} шт. X {self.price}{currency_symbol} " \
                  f"= {self.price * self.quantity}{currency_symbol}\n</code>"
        return result

    @classmethod
    async def get(cls, order_line_id: int):
        obj = await cls.query.where(
            and_(
                cls.id == order_line_id
            )).order_by(cls.id).gino.first()
        return obj

    @classmethod
    async def paginator(cls, order: Order, line_number=1):
        lines = await cls.query.where(
            and_(
                cls.order_id == order.id
            )).order_by(cls.id).gino.all()

        lines_count = len(lines)
        if line_number > lines_count:
            current_line = lines_count
        elif line_number < 1:
            current_line = 1
        else:
            current_line = line_number

        order_line = lines[current_line - 1]

        result = {
            'order_line': order_line,
            'page': {
                'first': 1,
                'previous': 1 if current_line == 1 else current_line - 1,
                'current': current_line,
                'next': current_line + 1 if current_line < lines_count else lines_count,
                'last': lines_count,
            }
        }

        return result

    async def set_quantity(self, quantity: int = 1):
        try:
            data_update = {}
            if quantity > 0:
                data_update = {'quantity': quantity, 'deleted_at': None}
            else:
                data_update = {'quantity': 0, 'deleted_at': func.now()}

            if data_update:
                await self.update(**data_update).apply()
            else:
                pass
        except UniqueViolationError:
            pass

    @classmethod
    async def add(cls, order: Order, product: Product, price: int, quantity: int = 1):
        try:
            current_lines = await cls.query.where(
                and_(cls.order_id == order.id, cls.product_id == product.id, cls.deleted_at is None)
            ).gino.all()
            # Если нет строк и количество больше 0, тогда добавить строку
            if quantity > 0 and len(current_lines) == 0:
                obj = OrderLine(order_id=order.id, product_id=product.id, quantity=quantity, price=price)
                await obj.create()
            elif quantity > 0 and len(current_lines) == 1:
                line = current_lines[0]
                line_update = {'quantity': quantity, 'price': price}
                if line_update:
                    await line.update(**line_update).apply()
            elif quantity == 0 and len(current_lines) == 1:
                line = current_lines[0]
                line_update = {'quantity': quantity, 'price': price, 'deleted_at': func.now()}
                if line_update:
                    await line.update(**line_update).apply()
                else:
                    pass
        except UniqueViolationError:
            pass
