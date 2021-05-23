from asyncpg import UniqueViolationError
from sqlalchemy import sql

from utils.db_api.database import BaseModel, db


# Сущности: заказ, товр, пользователь, строка заказа
class Entity(BaseModel):
    __tablename__ = "entities"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=False, default='')

    query: sql.select

    @classmethod
    async def get(cls, code: str):
        item = await cls.query.where(cls.code == code.lower()).gino.first()
        return item

    @classmethod
    async def add(cls, code: str, name: str = ''):
        try:
            obj = cls(code=code, name=name)
            await obj.create()
        except UniqueViolationError:
            pass

    @classmethod
    async def get_all(cls):
        objs = await cls.query.gino.all()
        return objs
