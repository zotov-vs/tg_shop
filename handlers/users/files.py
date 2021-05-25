import mimetypes
from ctypes import Union

from aiogram import types
from aiogram.types import ContentType, InputMediaPhoto

from loader import dp
from utils.db_api.models.files import File


@dp.message_handler(content_types=[ContentType.PHOTO])
async def answer_files(message: types.Message):
    if message.photo:
        content = message.photo[-1]  # Последняя фотка самого большого размера
    elif message.document:
        content = message.document
    else:
        return

    content_file = await content.download()
    file_obj = await File.add(file_name=content_file.name, customer_id=message.from_user.id,
                              file_unique_id=content.file_unique_id,
                              mime_type='image/jpeg')
    await message.reply(f"Дабавлен файл {file_obj.id}")


@dp.message_handler(content_types=[ContentType.DOCUMENT])
async def answer_files(message: types.Message):
    if message.photo:
        content = message.photo[-1]  # Последняя фотка самого большого размера
    elif message.document:
        content = message.document
    else:
        return

    content_file = await content.download()
    file_obj = await File.add(file_name=content_file.name, customer_id=message.from_user.id,
                              file_unique_id=content.file_unique_id, mime_type=content.mime_type)
    await message.reply(f"Дабавлен файл {file_obj.id}")
