import logging
import os
import re

from aiogram import Bot, types, md
from aiogram.utils.executor import start_webhook
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputMediaPhoto, InputMediaDocument
from urllib.request import urlopen
import json
import threading
import asyncio

import math, time
import datetime




from twilio.rest import Client



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



async def forward():
    hour = datetime.datetime.now().time().hour
    minute = datetime.datetime.now().time().minute

    dataJson=await bot.forward_message(admin_id, admin_id, 4)
    data = await bot.get_file(dataJson.document.file_id)
    data2 = bot.get_file_url(data.file_path)
    page_source = urlopen(data2).read()
    d = json.loads(page_source)
    for user in d['users']:
        for time in user['calltime']:

            if hour==time[0] and minute==time[1]:
                client = Client(account_sid, auth_token)
                call = client.calls.create(
                url='https://ex.ru',
                to='+79162721765',
                from_='+12027967603'
                )

                # call = client.calls.create(
                #     url='https://ex.ru',
                #     to='+79167105584',
                #     from_='+12027967603'
                # )
                #
                # call = client.calls.create(
                #     url='https://ex.ru',
                #     to='+79171673630',
                #     from_='+12027967603'
                # )

                user['calltime'].remove(time)
            # if hour > time[0]:
            #     user['calltime'].remove(time)

    with open('data3.json', 'w') as json_file:
        json.dump(d, json_file)
    with open('data3.json', 'rb') as f:
        await bot.edit_message_media(InputMediaDocument(f), admin_id, 4)


def printit():
    threading.Timer(60.0, printit).start()

    try:
        asyncio.run_coroutine_threadsafe(forward(),bot.loop)

    except asyncio.TimeoutError:
        print('The coroutine took too long, cancelling the task...')

    except Exception as exc:
        print(f'The coroutine raised an exception: {exc!r}')
    else:
        print(f'The coroutine returnr')


  # client = Client(account_sid, auth_token)
  # call = client.calls.create(
  #     url='https://ex.ru',
  #     to='+79162721765',
  #     from_='+12027967603'
  # )
  # print(call.sid)


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
    json2 = await bot.forward_message(admin_id, admin_id, 4)
    data = await bot.get_file(json2.document.file_id)
    data2 = bot.get_file_url(data.file_path)
    page_source = urlopen(data2).read()

    if message.text == 'clean':
        t0 = time.time()
        with open('data2.json', 'rb') as f:
            await bot.edit_message_media(InputMediaDocument(f), admin_id, 4)
        t1 = time.time()
        print(t1 - t0)


    if message.text=='tel':
        t0 = time.time()

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
                               'calltime': [[datetime.datetime.now().time().hour,datetime.datetime.now().time().minute+1]]})
            print(str(datetime.datetime.now().time))
            await bot.send_message(message.chat.id, 'You append')

            with open('data3.json', 'w') as json_file:
                json.dump(d, json_file)
            with open('data3.json', 'rb') as f:
                await bot.edit_message_media(InputMediaDocument(f), admin_id, 4)

        t1 = time.time()
        print(t1 - t0)
    try:
        time_user=int(re.search(r'\d+', message.text).group())
    except Exception:
        time_user=0

    if  time_user > 0:

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
                new_time=datetime.datetime.now()+datetime.timedelta(minutes=time_user)
                user['calltime'].append([new_time.time().hour,new_time.time().minute])
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
    printit()


    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=WEBAPP_HOST, port=WEBAPP_PORT)

    # executor.start_polling(dp, skip_updates=True)
