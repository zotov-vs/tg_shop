import asyncio

from asyncpg import UniqueViolationError
from sqlalchemy import Column, Integer, String, sql
from gino import Gino

from data.config import DB_CONNECTION_STRING
from utils.db_api.database import BaseModel, db


class Status(BaseModel):
    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_name = db.Column(db.String(50), unique=True)
    comment = db.Column(db.String(255), default='')

    query: sql.Select


async def add_status(name: str, comment: str = ''):
    try:
        status = Status(status_name=name, comment=comment)
        await status.create()
    except UniqueViolationError:
        pass


async def get_status(name: str):
    result = await Status.query.where(Status.status_name == name).gino.first()
    return result.id


