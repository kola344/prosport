import asyncio
import db
from aiogram import Bot, Dispatcher
import config
from tg_routers.admin.messages import router as admin_router

bot = Bot(token=config.tg_token)
dp = Dispatcher()
dp.include_router(admin_router)

async def main():
    await db.initialize()
    await dp.start_polling(bot)

asyncio.run(main())