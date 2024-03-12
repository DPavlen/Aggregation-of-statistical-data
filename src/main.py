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


# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Обработчик команды /start."""
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


# @dp.message()
# async def echo_handler(message: types.Message) -> None:
#     """
#     Handler will forward receive a message back to the sender
#     By default, message handler will handle all message types (like a text, photo, sticker etc.)
#     """
#     try:
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         await message.answer("Nice try!")


# @dp.register_message_handler(content_types=['text'])
@dp.message(F.text, Command("group"))
async def any_message(message: types.Message):
    msg_data = json.loads(message.text)
    dt_from = msg_data['dt_from']
    dt_upto = msg_data['dt_upto']
    group_type = msg_data['group_type']
    print(msg_data)
    result = main_app(dt_from, dt_upto, group_type)

    await bot.send_message(message.chat.id, result)
    # await message.answer(result)



async def main() -> None:
    # bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # await dp.start_polling(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())