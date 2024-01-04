import asyncio
import logging

import sqlite3 as sq

from aiohttp import ClientSession
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from DataBase import DataBase
from configs import BOT_TOKEN, API_URL, API_KEY

headers = {"x-api-key": API_URL}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def get_cat(url, headers):
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            cat_data = await response.json()
            return cat_data[0]["url"]


@dp.message(CommandStart)
async def start(message: types.Message):
    id = f'{message.chat.id}'
    # added in base id
    tg = DataBase("telegram.db")
    tg.insert("users", ('chat_id', ), (id,))
    
    await message.answer("Hello, my command is /cat")
    
    
@dp.message(Command("cat"))
async def send_cat(message: types.Message):
    cat_url = await get_cat(API_URL, headers)
    await bot.send_photo(message.chat.id, photo=cat_url)


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
