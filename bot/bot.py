import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from handlers import start

from middlewares.check_sub import CheckSubscription

from dotenv import load_dotenv
import os


load_dotenv(encoding='utf-8')

async def main():
    bot = Bot(os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    
    dp.message.middleware(CheckSubscription())
    
    dp.include_routers(
        start.router,
    )
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())