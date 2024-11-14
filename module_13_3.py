from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(text=['Здравствуйте', 'Привет'])
async def hello_message(message):
    print("Здравствуйте! Введите команду /start, чтобы начать общение.")
    await message.answer("Здравствуйте! Введите команду /start, чтобы начать общение.")


@dp.message_handler(commands=['start'])
async def start_message(message):
    print("Привет! Я бот помогающий твоему здоровью!")
    await message.answer("Привет! Я бот помогающий твоему здоровью!")


@dp.message_handler()
async def all_message(message):
    print("Введите команду /start, чтобы начать общение.")
    await message.answer("Я пока не понимаю Вашей команды... Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
