from sqlalchemy import sql

from utils.db_api.database import BaseModel, db, TimedBaseModel


class Promocode(TimedBaseModel):
    __tablename__ = "promocodes_to_customers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customers.id'), nullable=False)
    pormocode_id = db.Column(db.Integer, db.ForeignKey('pormocodes.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    day_expire = db.Column(db.Integer, default=7)
    start = db.Column(db.Date, default='2020-01-01')
    finish = db.Column(db.Date, default='2099-12-31')
    discount_percent = db.Column(db.Integer, nullable=True)
    discount_amount = db.Column(db.Integer, nullable=True)

    query: sql.Select

    @classmethod
    async def get(cls, code: str):
        item = await cls.query.where(cls.code == code.upper()).gino.first()
        return item
