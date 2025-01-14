from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = 
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler()
async def all_message(message):
    print(f"Мы получили сообщение {message}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
