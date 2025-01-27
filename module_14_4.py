# Домашнее задание по теме "Доработка бота"

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
btn_buy = KeyboardButton(text="Купить")
btn_info = KeyboardButton(text="Информация")
kb.add(btn_calc)
kb.add(btn_buy)
kb.add(btn_info)

kbi = InlineKeyboardMarkup(resize_keyboard=True)
btn_calories = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
btn_formula = InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
kbi.add(btn_calories)
kbi.add(btn_formula)

kbi_buy = InlineKeyboardMarkup(resize_keyboard=True)
btn_product1 = InlineKeyboardButton(text="Product1", callback_data="product_buying")
btn_product2 = InlineKeyboardButton(text="Product2", callback_data="product_buying")
btn_product3 = InlineKeyboardButton(text="Product3", callback_data="product_buying")
btn_product4 = InlineKeyboardButton(text="Product4", callback_data="product_buying")
kbi_buy.add(btn_product1)
kbi_buy.add(btn_product2)
kbi_buy.add(btn_product3)
kbi_buy.add(btn_product4)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=kb)


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=kbi)


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for i in range(4):
        await message.answer(f"Название: Product{i} | Описание: описание {i} | Цена: {i * 100}")
        with open(f"photo/img{i}.jpg", "rb") as photo:
            await message.answer_photo(photo)
    await message.answer("Выберите продукт для покупки:", reply_markup=kbi_buy)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("Формула Миффлина-Сан Жеора: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5.")
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    try:
        await message.answer(
            f"Ваша норма калорий: {10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5}")
    except:
        await message.answer(f"Что-то пошло не так, возможно введены не числовые значения.")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
