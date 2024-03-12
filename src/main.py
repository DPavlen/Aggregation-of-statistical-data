import asyncio
import logging
import json
import os
import sys

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from data_of_mongodb import main_app

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Обработчик команды /start."""
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message(F.text, Command("group"))
async def any_message(message: types.Message)-> None:
    # Проверка наличия текста в сообщении
    if not message.text:
        await message.answer("The message is empty.")
        return

    try:
        msg_data = json.loads(message.text)
        dt_from = msg_data['dt_from']
        dt_upto = msg_data['dt_upto']
        group_type = msg_data['group_type']
        print(msg_data)
        result = main_app(dt_from, dt_upto, group_type)
        await bot.send_message(message.chat.id, result)
    except json.JSONDecodeError as e:
        await message.answer(f"Error decoding JSON: {e}")



async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())