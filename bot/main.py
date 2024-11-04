import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import start, admin
from Data.db import drop_tables, init_db, get_session  # Импортируем функцию получения сессии
from decouple import config

bot = Bot(token=config('BOT_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

CHANNEL_ID = config('ChanelName')  # ID или @username вашего канала

# Функция для проверки подписки
async def check_user_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as ex:
        print(ex)

async def on_startup(dispatcher: Dispatcher):
    # await drop_tables() # Отчистка БД
    await init_db()  # Инициализация базы данных
    

async def main():
    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.startup.register(on_startup)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
