import logging
import os
from aiogram import Bot, types, md
from aiogram.utils.executor import start_webhook
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputMediaPhoto, InputMediaDocument
import time
from urllib.request import urlopen
import json
import threading
import asyncio
import aiotools
import math, time
from async_cron.job import CronJob
from async_cron.schedule import Scheduler

from twilio.rest import Client

from twilio.rest import Client



async def test(*args, **kwargs):
    print(args, kwargs)


def tt(*args, **kwargs):
    print(args, kwargs)



async def async_function():
    print("Hello, World!")



def printit():

  json2 =   bot.forward_message(admin_id, admin_id, 4)
  # data =  bot.get_file(json2.document.file_id)
  # data2 = bot.get_file_url(data.file_path)
  # page_source = urlopen(data2).read()
  # d = json.loads(page_source)
  # for user in d['users']:
  #
  #   print(user['chatid'])

  # client = Client(account_sid, auth_token)
  # call = client.calls.create(
  #     url='https://ex.ru',
  #     to='+79162721765',
  #     from_='+12027967603'
  # )
  # print(call.sid)

  print ("Hello, World!")

account_sid = 'AC52a194acef951b3b36e94f294d836ae6'
auth_token = '988090f0870502e26899be8b5aeb41f0'

TOKEN = '891139186:AAEVLHlMc2dt5SAPKtCeQ-Jli_rnSIyC9eU'


WEBHOOK_HOST = 'https://tel-bot-python.herokuapp.com'  # name your app
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
admin_id=852450369


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
    # with open('data.json', 'rb') as f:
    #     print(f)
    #     await bot.send_document(message.chat.id, f)


    if message.text=='tel':
        t0 = time.time()
        json2 = await bot.forward_message(admin_id, admin_id, 4)
        data = await bot.get_file(json2.document.file_id)
        data2 = bot.get_file_url(data.file_path)
        page_source = urlopen(data2).read()


        metka = False
        d = json.loads(page_source)
        print(len(d['users']))
        for user in d['users']:

            if user['chatid'] == message.chat.id:
                await bot.send_message(message.chat.id, 'You here')
                metka = True
                break
        if metka == False:
            d['users'].append({'chatid': message.chat.id,
                               'phones': 8917,
                               'state': 0,
                               'calltime': ['jd@example.com', 'jd@example.org']})
            await bot.send_message(message.chat.id, 'You append')

            with open('data3.json', 'w') as json_file:
                json.dump(d, json_file)
            with open('data3.json', 'rb') as f:
                await bot.edit_message_media(InputMediaDocument(f), admin_id, 4)

        t1 = time.time()
        print(t1 - t0)

    else:

        json2 = await bot.forward_message(admin_id, admin_id, 4)
        data = await bot.get_file(json2.document.file_id)
        data2 = bot.get_file_url(data.file_path)
        page_source = urlopen(data2).read()
        #
        d = json.loads(page_source)
        # for number in range(100):
        #     d['users'].append({'chatid': number,
        #                        'phones': 8917,
        #                        'state': 0,
        #                        'calltime': ['jd@example.com', 'jd@example.org']})
        #
        # with open('data3.json', 'w') as json_file:
        #     json.dump(d, json_file)
        # with open('data3.json', 'rb') as f:
        #     await bot.edit_message_media(InputMediaDocument(f), admin_id, 4)
        print(len(d['users']))
        t0 = time.time()
        for user in d['users']:
            if user['chatid'] == message.chat.id:
                await bot.send_message(message.chat.id, 'You here')
                print(user)
                user['phones'] = 2
                with open('data3.json', 'w') as json_file:
                    json.dump(d, json_file)
                with open('data3.json', 'rb') as f:
                    await bot.edit_message_media(InputMediaDocument(f), admin_id, 4)

                break




        t1 = time.time()
        print(t1 - t0)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    # insert code here to run it before shutdown
    pass


if __name__ == '__main__':
    # threading.Timer(5.0, printit).start()
    msh = Scheduler()
    myjob = CronJob(name='test', run_total=100).every(
        5).second.go(test, (1, 2, 3), name=123)

    msh.add_job(myjob)


    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=WEBAPP_HOST, port=WEBAPP_PORT)
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(msh.start())
    except KeyboardInterrupt:
        print('exit')
    # executor.start_polling(dp, skip_updates=True)
