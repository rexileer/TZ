import os
import sys

# Добавляем корень проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Это добавит корень проекта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})

import django
django.setup()


import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from handlers import start, catalog, cart, delivery_fsm, faq, broadcast
from middlewares.check_sub import CheckSubscription

from dotenv import load_dotenv

import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (INFO для обычных сообщений)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат логов
    handlers=[
        logging.StreamHandler(),  # Вывод логов в консоль
        logging.FileHandler('bot_logs.log', mode='a')  # Запись логов в файл 'bot_logs.log'
    ]
)

# Получение логгера
logger = logging.getLogger(__name__)


load_dotenv(encoding='utf-8')

async def main():
    bot = Bot(os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    
    dp.message.middleware(CheckSubscription())
    
    dp.include_routers(
        start.router,
        catalog.router,
        cart.router,
        delivery_fsm.router,
        faq.router,
        broadcast.router,
    )
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())