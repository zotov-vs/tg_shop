import uuid
from datetime import timedelta, datetime
from pytz import timezone

from asyncpg import UniqueViolationError
from sqlalchemy import and_, sql

from utils.db_api.database import TimedBaseModel, db
from utils.db_api.models.orders import Order


class Bill(TimedBaseModel):
    __tablename__ = "bills"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(36), unique=True)
    customer_id = db.Column(db.BigInteger, db.ForeignKey("customers.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    amount = db.Column(db.Integer)
    status_id = db.Column(db.Integer, db.ForeignKey("statuses.id"))
    date_expire = db.Column(db.TIMESTAMP)
    comment = db.Column(db.String(255), default='')

    query: sql.Select

    @classmethod
    async def add(cls, order: Order, minutes=10, comment=''):
        try:
            if order.total >= 1:
                uid = str(uuid.uuid4())

                date_expire = datetime.now() + timedelta(minutes=minutes)

                if not comment:
                    comment = f"Заказ #{order.id}"

                obj = Bill(uid=uid, customer_id=order.customer_id, order_id=order.id, amount=order.total,
                           status_id=1, date_expire=date_expire, comment=comment)
                await obj.create()
                return obj
        except UniqueViolationError:
            pass

    @classmethod
    async def get_or_add(cls, order: Order, minutes=10, comment=''):
        obj = await cls.get(order)
        if not obj:
            obj = await cls.add(order=order, minutes=minutes, comment=comment)
        return obj

    @classmethod
    async def get(cls, order: Order):
        obj = await cls.query.where(
            and_(
                cls.order_id == order.id,
                cls.date_expire < datetime.utcnow()
            )
        ).gino.first()

        return obj
