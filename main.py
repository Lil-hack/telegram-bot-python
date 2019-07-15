import logging
import os
from aiogram import Bot, types, md
from aiogram.utils.executor import start_webhook
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputMediaPhoto, InputMediaDocument
import time
from urllib.request import urlopen
import json

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
        t0 = time.time()
        json2 = await bot.forward_message(admin_id, admin_id, 4)
        data = await bot.get_file(json2.document.file_id)
        data2 = bot.get_file_url(data.file_path)
        page_source = urlopen(data2).read()

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

        for user in d['users']:
            if user['chatid'] == message.chat.id:
                await bot.send_message(message.chat.id, 'You here')
                print(user)
                user['phones'] = 2
                # with open('data3.json', 'w') as json_file:
                #     json.dump(d, json_file)
                # with open('data3.json', 'rb') as f:
                #     await bot.edit_message_media(InputMediaDocument(f), admin_id, 4)

                break




        t1 = time.time()
        print(t1 - t0)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    # insert code here to run it before shutdown
    pass


if __name__ == '__main__':
    # start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
    #               on_startup=on_startup, on_shutdown=on_shutdown,
    #               host=WEBAPP_HOST, port=WEBAPP_PORT)
    executor.start_polling(dp, skip_updates=True)