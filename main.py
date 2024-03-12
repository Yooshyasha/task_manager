import asyncio

from Handlers.database import DatabaseControl
from Handlers.messages import message_router
from Handlers.callbacks import callbacks_router

from loader import Program

from aiogram import Dispatcher

bot = Program().bot
dp = Dispatcher()

dp.include_routers(
    message_router,
    callbacks_router
)


async def main():
    DatabaseControl().start()
    while True:
        await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
