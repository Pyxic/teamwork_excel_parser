import asyncio
import io
import logging
import os.path

from aiogram.methods import GetFile
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command
from aiogram.types import Message, File, InputFile, BufferedInputFile

from config import BOT_TOKEN
from xlsx_parser import TeamworkExcelParser

# Bot token can be obtained via https://t.me/BotFahter
TOKEN = BOT_TOKEN

# All handlers should be attached to the Router (or Dispatcher)
router = Router()
bot = Bot(TOKEN, parse_mode="HTML")

@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, <b>{message.from_user.full_name}!</b>. Use this bot to fill in the summary table."
                         f"Export an excel file (xls, xlsx) from teamwork and upload it here.")


@router.message(F.content_type.in_({'document'}))
async def file_handler(message: Message):
    file = message.document
    if not file.file_name.endswith(('.xlsx', '.xls')):
        await message.answer("load only xls, xlsx files")
        return
    uploaded_file = await bot.get_file(file.file_id)
    downloaded_file = await bot.download_file(uploaded_file.file_path)
    # temp_path = os.path.join(os.getcwd(), file.file_name)
    # with open(uploaded_file.file_path, 'rb') as f:
    try:
        new_excel_file = TeamworkExcelParser(downloaded_file, file.file_name).get_valid_format()
    except Exception as e:
        await message.answer("not valid file data")
        return
    new_excel_file.seek(0)
    new_file = BufferedInputFile(new_excel_file.read(), "report.xlsx")
    print(new_file.data)
    # with open("temp.xlsx", 'rb') as temp_file:
    #     new_file = InputFile("temp.xlsx")
    await bot.send_document(chat_id=message.chat.id, document=new_file)


@router.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward received message back to the sender

    By default, message handler will handle all message types (like text, photo, sticker and etc.)
    """
    try:
        # Send copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())