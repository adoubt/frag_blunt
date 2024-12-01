pip install aiogram

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

API_TOKEN = 'YOUR_API_TOKEN'  # Замените на ваш токен от бота

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я простой бот на aiogram!")

# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Этот бот может ответить на команды /start и /help.")

# Обработчик текстовых сообщений
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f"Ты сказал: {message.text}")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
