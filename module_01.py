from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = "7086380332:AAH2ULiaxQS6SRcG_Csc82KIMDs1T1PZQHg"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler()
async def all_message(message):
    print(f"Мы получили сообщение")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
