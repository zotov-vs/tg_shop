from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.db_api import database, database_init

from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):

    await database.on_startup(dispatcher)
    await database_init.on_startup(dispatcher)


    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
