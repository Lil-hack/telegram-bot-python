import logging
import os
from aiogram import Bot, types, md
from aiogram.utils.executor import start_webhook
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputMediaPhoto, InputMediaDocument
import time
from urllib.request import urlopen
import json

TOKEN = '873656324:AAFqF5d_0oAMgN2F2XPW5xMjrGULZvUnZTI'


WEBHOOK_HOST = 'https://tel-bot-python.herokuapp.com'  # name your app
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def welcome(message: types.Message):
    await bot.send_message(
        message.chat.id,
        f'Приветствую! Это демонтрационный бот\n'
        f'Подробная информация на '
        f'{md.hlink("github", "https://github.com/deploy-your-bot-everywhere/heroku")}',
        parse_mode=types.ParseMode.HTML,
        disable_web_page_preview=True)


@dp.message_handler()
async def echo(message: types.Message):
    with open('data.json', 'rb') as f:
        print(f)
        await bot.send_document(message.chat.id, f)

    t0 = time.time()

    json2 = await bot.forward_message(message.chat.id, message.chat.id, message.message_id + 1)
    data = await bot.get_file(json2.document.file_id)
    data2 = bot.get_file_url(data.file_path)

    page_source = urlopen(data2).read()
    print(page_source)
    d = json.loads(page_source)

    with open('data3.json', 'w') as json_file:
        json.dump(d, json_file)

    with open('data3.json', 'rb') as f:
        await bot.edit_message_media(InputMediaDocument(f), message.chat.id, message.message_id + 1)

    t1 = time.time()

    print(t1 - t0)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    # insert code here to run it before shutdown
    pass


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=WEBAPP_HOST, port=WEBAPP_PORT)
