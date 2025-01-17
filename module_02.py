# Домашнее задание по теме "Методы отправки сообщений"

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = "При отправке вашего кода на GitHub не забудьте убрать ключ для подключения к вашему боту!"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def massages_one(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.")


@dp.message_handler()
async def massages_two(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
