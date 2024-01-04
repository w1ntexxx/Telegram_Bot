import os
import asyncio
import logging

import sqlite3 as sq

from aiohttp import ClientSession
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from DataBase import DataBase
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv(os.getenv("TOKEN"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def get_cat(url, headers):
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            cat_data = await response.json()
            return cat_data[0]["url"]


@dp.message(Command("cat"))
async def send_cat(message: types.Message):
    cat_url = await get_cat(api_url, headers)
    await bot.send_photo(message.chat.id, photo=cat_url)


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


# if __name__ == "__main__":
#     asyncio.run(main())
