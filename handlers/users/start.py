from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.main import main_keyboard
from loader import dp, bot
from utils.db_api.models.custumers import add_customer


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):

    deep_link_args = message.get_args()
    await add_customer(message.from_user, deep_link_args)
    discount = 10
    promocode = 15
    bonuses = 300
    text = f'Привет 👋, {message.from_user.full_name}!\n\n' \
           f'Мы продаем <b>выгодные</b> тарифы для основных сотовых операторов РФ 🇷🇺\n' \
           f'Каталог с тарифами в меню 👇\n\n' \
           f'Ваша личная скидка  : <code>{discount}%</code>\n' \
           f'Скидка по промокоду : <code>{promocode}%</code>\n' \
           f'Сумма на бонусном счете: <code>{bonuses}₽</code> \n'
    await message.answer(text, reply_markup=main_keyboard)
# Проверить подписку на каналы
# Выслать реферальную ссылку
    bot = await dp.bot.me
    bot_username = bot.username
    referral_text = f'{message.from_user.full_name}, \n' \
                    f'ваш реферальный код: <code>{message.from_user.id}</code> \n' \
                    f'ссылка: https://t.me/{bot_username}?start={message.from_user.id} \n' \
                    f'Перешлите сообщение своим друзьям и они получат Вашу личную скидку в размере' \
                    f' <code>{discount}%</code> сразу после активации в боте и подписке на основной канал'
    referral_text2 = f'А вы будите получать <code>10%</code> кэшбэка на ваш счет с их покупок 😎'

    await message.answer(referral_text)
    await message.answer(referral_text2)





