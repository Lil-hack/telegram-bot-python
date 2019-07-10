import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputMediaPhoto, InputMediaDocument
import time
from urllib.request import urlopen
import json
from io import BytesIO

API_TOKEN = '873656324:AAFqF5d_0oAMgN2F2XPW5xMjrGULZvUnZTI'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when client send `/start` or `/help` commands.
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo, caption='Cats is here 😺',
                             reply_to_message_id=message.message_id)


@dp.message_handler()
async def echo(message: types.Message):
    with open('data.json', 'rb') as f:
        print(f)
        await bot.send_document(message.chat.id,f)

    t0 = time.time()

    json2= await bot.forward_message(message.chat.id, message.chat.id,message.message_id+1)
    data = await bot.get_file(json2.document.file_id)
    data2 =  bot.get_file_url(data.file_path)

    page_source = urlopen(data2).read()
    print(page_source)
    d = json.loads(page_source)

    with open('data3.json', 'w') as json_file:
        json.dump(d, json_file)

    with open('data3.json', 'rb') as f:
         await bot.edit_message_media(InputMediaDocument(f), message.chat.id, message.message_id+1)


    t1 = time.time()

    print(t1-t0)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)