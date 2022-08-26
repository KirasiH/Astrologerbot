from aiogram import Bot, Dispatcher
from handlers import register_client
from prognosclass import prognos
from dispatch import mailing
from dotenv import load_dotenv, find_dotenv
import aioschedule
import logging
import asyncio
import os

load_dotenv(find_dotenv())

bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher()


async def scheduler():

    aioschedule.every().day.at("0:12").do(mailing, bot)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():

    dp.include_router(register_client())

    prognos.create_prognos()

    asyncio.create_task(scheduler())

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.run(main())
