import flask
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputMediaPhoto, InputMediaDocument
import time
from urllib.request import urlopen
import json



from config import *

import os

server = flask.Flask(__name__)

API_TOKEN = '873656324:AAFqF5d_0oAMgN2F2XPW5xMjrGULZvUnZTI'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



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
@server.route('/' + TOKEN, methods=['POST'])
def get_message():
   
    return "!", 200


@server.route('/', methods=["GET"])
def index():

    # executor.set_webhook(dp,url="https://{}.herokuapp.com/{}".format(APP_NAME, TOKEN))
    return "Hello from Heroku!", 200


if __name__ == "__main__":

    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
