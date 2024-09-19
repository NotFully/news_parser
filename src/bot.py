import asyncio
from aiogram import types

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from middlewares.access import CheckUserHaveAccess
from handlers import (
    start,
    menu,
    mychannels,
    keyword,
    news
)

from utils.db.db import DB
from utils.parsing import Parser
from utils.config import BOT_KEY


bot = Bot(token=BOT_KEY)
dp = Dispatcher()


def setup(dp: Dispatcher):
    db = DB()
    db.create_table()

    dp.include_routers(
        start.router,
        menu.router,
        mychannels.router,
        keyword.router,
        news.router
    )
    dp.message.middleware(CheckUserHaveAccess())


def additional_tasks(bot, dp):
    scheduler = AsyncIOScheduler()
    parser = Parser(bot=bot, dp=dp)

    # парсить каждый час!
    scheduler.add_job(parser.start, 'cron', minute='52')  # будем запускать заранее, чтобы успел напарсить до 00
    scheduler.start()


async def main():
    setup(dp)
    additional_tasks(bot=bot, dp=dp)

    print('bot started')

    await bot.get_updates(timeout=10)
    await dp.start_polling(bot, polling_timeout=11)


if __name__ == "__main__":
    asyncio.run(main())

