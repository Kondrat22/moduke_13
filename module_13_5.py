from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = "_______________________"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button1, button2)


class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def set_gender(message):
    await message.answer("Введите свой пол [м/ж]:")
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender, text=['М', 'м', 'Ж', 'ж'])
async def set_age(message, state):
    await state.update_data(gender=message.text.lower())
    await message.answer("Введите свой возраст (полных лет):")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост (см.):")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес (кг.):")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    raw_calories = 10 * int(data['weight']) + 6.25 * \
        int(data['growth']) - 5 * int(data['age'])
    if data['gender'] == 'м':
        result = raw_calories + 5
        await message.answer(f"Оптимальное количество калорий: {result}")
    elif data['gender'] == 'ж':
        result = raw_calories - 161
        await message.answer(f"Оптимальное количество калорий: {result}")

    await state.finish()


@dp.message_handler(text=['Здравствуйте', 'Привет'])
async def hello_message(message):
    #    print("Здравствуйте! Введите команду /start, чтобы начать общение.")
    await message.answer("Здравствуйте! Введите команду /start, чтобы начать общение.")


@dp.message_handler(text=['Информация'])
async def info_message(message):
    await message.answer("Этот бот был создан Владимиром Кондратом")


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    print("Кто-то нажал на старт)")
    await message.answer("Привет! Я бот помогающий твоему здоровью! Нажмите на кнопку Рассчитать и я для Вас рассчитаю необходимое количество килокалорий (ккал) в сутки.", reply_markup=kb)


@dp.message_handler()
async def all_message(message):
    #    print("Введите команду /start, чтобы начать общение.")
    await message.answer("Я пока не понимаю Вашей команды... Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
