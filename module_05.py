# Домашнее задание по теме "Инлайн клавиатуры".

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api = "При отправке вашего кода на GitHub не забудьте убрать ключ для подключения к вашему боту!"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()  # возраст
    growth = State()  # рост
    weight = State()  # вес


kb = ReplyKeyboardMarkup(resize_keyboard=True)
btn_calc = KeyboardButton(text="Рассчитать")
btn_info = KeyboardButton(text="Информация")
kb.add(btn_calc)
kb.add(btn_info)

kbi = ReplyKeyboardMarkup(resize_keyboard=True)
btn_calories = KeyboardButton(text="Рассчитать норму калорий")
btn_formula = KeyboardButton(text="Формулы расчёта")
kbi.add(btn_calories)
kbi.add(btn_formula)


@dp.message_handler(commands=['start'])
async def hello(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=kb)


@dp.message_handler(text="Рассчитать")
async def get_formulas(message):
    await message.answer("Выберите опцию:", reply_markup=kbi)
    await UserState.age.set()


@dp.message_handler(text="Рассчитать")
async def get_age(message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def get_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def get_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def norm_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    try:
        await message.answer(
            f"Ваша норма калорий:{10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5}")
    except:
        await message.answer(f"Что-то пошло не так, возможно введены не числовые значения.")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
