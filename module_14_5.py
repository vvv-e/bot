# Домашнее задание по теме "Написание примитивной ORM"

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio
from crud_functions import get_all_products, is_included, add_user
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# получить список продуктов из БД
products = get_all_products()

api = "При отправке вашего кода на GitHub не забудьте убрать ключ для подключения к вашему боту!"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()  # возраст
    growth = State()  # рост
    weight = State()  # вес


class RegistrationState(StatesGroup):
    username = State()  # имя
    email = State()  # эл.почта
    age = State()  # возраст
    balance = 1000  # баланс


kb = ReplyKeyboardMarkup(resize_keyboard=True)
btn_calc = KeyboardButton(text="Рассчитать")
btn_buy = KeyboardButton(text="Купить")
btn_reg = KeyboardButton(text="Регистрация")
btn_info = KeyboardButton(text="Информация")
kb.add(btn_calc)
kb.add(btn_buy)
kb.add(btn_reg)
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
    for prod in products:
        await message.answer(f"Название: {prod[1]} | Описание: {prod[2]} | Цена: {prod[3]}")
        with open(f"photo/img{prod[0] - 1}.jpg", "rb") as photo:
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


@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(username=message.text)
    await message.answer("Введите свой email:")
    await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=UserState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    try:
        add_user(data['username'], data['email'], data['age'])
    except:
        await message.answer(f"Что-то пошло не так, данные не занесены в таблицу Users.")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
