from typing import List

import asyncio
import sqlalchemy as sa
from aiogram import Dispatcher
from gino import Gino
from loguru import logger
from sqlalchemy import Column
from sqlalchemy import DateTime, TIMESTAMP
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String

from data.config import DB_CONNECTION_STRING

db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True),
                        default=func.now(),
                        server_default=func.now())

    updated_at = Column(DateTime(timezone=True),
                        default=func.now(),
                        onupdate=func.now(),
                        server_default=func.now())

    deleted_at = Column(DateTime(timezone=True), nullable=True)


async def on_startup(dispatcher: Dispatcher):
    logger.info("Setup PostgreSQL Connection")
    await db.set_bind(DB_CONNECTION_STRING)
    # logger.info("drop_all")
    # await db.gino.drop_all()
    logger.info("create_all")
    await db.gino.create_all()


async def on_shutdown(dispatcher: Dispatcher):
    bind = db.pop_bind()
    if bind:
        logger.info("Close PostgreSQL Connection")
        await bind.close()
