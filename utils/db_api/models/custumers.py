from aiogram import types
from asyncpg import UniqueViolationError
from sqlalchemy import Column, BigInteger, String, sql, Boolean, Integer, ForeignKey


from utils.db_api.database import TimedBaseModel, BaseModel, db
from utils.db_api.models.statuses import get_status


class Custumer(TimedBaseModel):
    __tablename__ = 'customers'

    id = db.Column(BigInteger, primary_key=True)
    name = db.Column(String(200))
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=False)
    referral_id = db.Column(db.BigInteger, default=0)
    is_admin = db.Column(db.Boolean, default=False)
    is_manager = db.Column(db.Boolean, default=False)
    is_supplier = db.Column(db.Boolean, default=False)

    query: sql.Select


async def add_customer(tg_user: types.User, deep_link_args: str):
    try:
        referral_id = 0
        if deep_link_args.isdigit():
            referral_id = int(deep_link_args)
        elif deep_link_args.isalnum():
            # get_promocode(deep_link_args)
            pass

        status_id = get_status('Посетитель')
        user = Custumer(id=tg_user.id, name=tg_user.full_name, referral_id=referral_id, status_id=status_id)
        await user.create()
    except UniqueViolationError:
        pass