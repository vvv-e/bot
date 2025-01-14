from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = ''.join(
    ['7', '0', '8', '6', '3', '8', '0', '3', '3', '2', ':', 'A', 'A', 'H', '2', 'U', 'L', 'i', 'a', 'x', 'Q', 'S',
     '6', 'S', 'R', 'c', 'G', '_', 'C', 's', 'c', '8', '2', 'K', 'I', 'M', 'D', 's', '1', 'T', '1', 'P', 'Z', 'Q',
     'H', 'g'])
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler()
async def all_message(message):
    print(f"Мы получили сообщение {message}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
