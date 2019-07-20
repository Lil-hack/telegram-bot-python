import logging
import os
import re

from aiogram import Bot, types, md
from aiogram.utils.executor import start_webhook
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputMediaPhoto, InputMediaDocument, KeyboardButton, ReplyKeyboardMarkup, ContentType
from urllib.request import urlopen
import json
import threading
import asyncio

import time
import datetime

from twilio.rest import Client

from name import *

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
heroku_start=False



async def timer_logic():
    hour = datetime.datetime.now().time().hour+3
    minute = datetime.datetime.now().time().minute

    data = await get_data()
    print(hour,':',minute)
    for user in data['users']:
        for time in user['calltime']:

            if hour==time[0] and minute==time[1]:

                client = Client(account_sid, auth_token)
                client.calls.create(
                url='https://ex.ru',
                to=user['phones'],
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

    await save_data(data)


def timer_start():
    threading.Timer(60.0, timer_start).start()

    try:
        asyncio.run_coroutine_threadsafe(timer_logic(),bot.loop)
    except Exception as exc:
        print(f'The coroutine raised an exception: {exc!r}')


async def get_data():
    forward_data = await bot.forward_message(admin_id, admin_id, 4)
    file_data = await bot.get_file(forward_data.document.file_id)
    file_url_data = bot.get_file_url(file_data.file_path)
    json_file= urlopen(file_url_data).read()
    return json.loads(json_file)

async def save_data(data):
    with open('data3.json', 'w') as json_file:
        json.dump(data, json_file)
    with open('data3.json', 'rb') as f:
        await bot.edit_message_media(InputMediaDocument(f), admin_id, 4)


@dp.message_handler(commands='start')
async def welcome(message: types.Message):
    button = KeyboardButton(B_REGISTRER)
    button.request_contact = True
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
    await bot.send_message(
        message.chat.id,
        f'Приветствую! Это демонтрационный бот',
        reply_markup=kb)



@dp.message_handler(content_types=ContentType.CONTACT)
async def registration(message: types.Message):
    print(message.contact.phone_number)
    t0 = time.time()

    metka = False
    data = await get_data()
    print(len(data['users']))
    for user in data['users']:

        if user['chatid'] == message.chat.id:
            await bot.send_message(message.chat.id, 'You here')
            metka = True
            break
    if metka == False:
        data['users'].append({'chatid': message.chat.id,
                           'phones': message.contact.phone_number,
                           'state': 0,
                           'calltime': [[datetime.datetime.now().time().hour+3,datetime.datetime.now().time().minute+1]]})
        print(str(datetime.datetime.now().time))
        button0 = KeyboardButton(B_CALL_NOW)
        button = KeyboardButton(B_CLEAN)
        button2 = KeyboardButton(B_LIST_CALLS)
        button3 = KeyboardButton(B_INFO)
        kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button0).row(button,button2).add(button3)

        await bot.send_message(message.chat.id, 'Вы удачно зарегистрирвоались', reply_markup=kb)

        await save_data(data)


    t1 = time.time()
    print(t1 - t0)

@dp.message_handler()
async def main_logic(message: types.Message):

    t0 = time.time()
    # with open('data.json', 'rb') as f:
    #     print(f)
    #     await bot.send_document(message.chat.id, f)

    data = await get_data()
    metka2=False
    for user in data['users']:
        if user['chatid'] == message.chat.id:
            time_user=[]
            try:
                for stroka in message.text.split(':'):
                    time_user.append(int(re.search(r'\d+',stroka).group()))

            except Exception as ex:
                print(ex)

            print(time_user)
            if len(time_user)==1:
                if time_user[0] > 0 and time_user[0] < 120:

                    new_time = datetime.datetime.now() + datetime.timedelta(minutes=time_user[0])

                    metka_time = False
                    for time_us in user['calltime']:
                        if (new_time.time().hour + 3) == time_us[0] and new_time.time().minute == time_us[1]:
                            await bot.send_message(message.chat.id, 'На данное время у Вас уже записан звонок')
                            metka_time=True
                            break
                    if metka_time==False:
                        user['calltime'].append([new_time.time().hour + 3, new_time.time().minute])
                        await save_data(data)
                        await bot.send_message(message.chat.id,  'Вы добавили звонок на {}:{}'
                                               .format(str(new_time.time().hour + 3),str(new_time.time().minute)))
                else:
                    await bot.send_message(message.chat.id, 'Укажите время от 1 до 120 минут')
            if len(time_user)==2:
                if time_user[0] >= 0 and time_user[0] <= 24 and time_user[1] >= 0 and time_user[1] <= 60:


                    metka_time = False
                    for time_us in user['calltime']:
                        if time_user[0] == time_us[0] and time_user[1] == time_us[1]:
                            await bot.send_message(message.chat.id,'На данное время уже запланирован звонок')
                            metka_time = True
                            break
                    if metka_time == False:
                        user['calltime'].append([time_user[0], time_user[1]])
                        await save_data(data)
                        await bot.send_message(message.chat.id, 'Вы добавили звонок на {}:{}'
                                               .format(str(time_user[0]),str(time_user[1])))
                else:
                    await bot.send_message(message.chat.id, 'Вы указали неправильное время. Попробуйте занова.')


            if message.text == B_CLEAN:
                user['calltime'].clear()
                await save_data(data)
                await bot.send_message(message.chat.id, 'Все звонки удачно сброшены.')

            if message.text == B_CALL_NOW:
                client = Client(account_sid, auth_token)
                client.calls.create(
                    url='https://ex.ru',
                    to=user['phones'],
                    from_='+12027967603'
                )

            if message.text == B_LIST_CALLS:
                if len(user['calltime'])==0:
                    await bot.send_message(message.chat.id, 'У Вас нет запланированных звонков')
                else:
                    str_call_list='Запланированные звонки:\n'
                    for time_call in user['calltime']:
                        str_call_list+=str(time_call[0])+':'+str(time_call[1])+'\n'
                    await bot.send_message(message.chat.id, str_call_list)
            if message.text == B_INFO:
                await bot.send_message(message.chat.id, 'Инфо тут')


            metka2 = True
            break
    if metka2==False:
        button = KeyboardButton(B_REGISTRER)
        button.request_contact = True
        kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
        await bot.send_message(message.chat.id, 'Вы не зарегистрированы, нажмите на кнопку "Регистрация"', reply_markup=kb)

    if message.text == 'clean':
        with open('data2.json', 'rb') as f:
            await bot.edit_message_media(InputMediaDocument(f), admin_id, 4)

    if message.text == 'add':
        for number in range(100):
            data['users'].append({'chatid': number,
                               'phones': 8917,
                               'state': 0,
                               'calltime': []})

        with open('data3.json', 'w') as json_file:
            json.dump(data, json_file)
        with open('data3.json', 'rb') as f:
            await bot.edit_message_media(InputMediaDocument(f), admin_id, 4)

    t1 = time.time()
    print(t1 - t0)





async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    # insert code here to run it before shutdown
    pass


if __name__ == '__main__':
    timer_start()

    if heroku_start:
        start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                      on_startup=on_startup, on_shutdown=on_shutdown,
                      host=WEBAPP_HOST, port=WEBAPP_PORT)
    else:
        executor.start_polling(dp, skip_updates=True)
