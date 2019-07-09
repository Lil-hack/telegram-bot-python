from flask import Flask, jsonify
app = Flask(__name__)
from telebot import types, TeleBot

import os
<<<<<<< HEAD
from twilio.rest import Client
import time
from twilio.rest import Client

account_sid = 'AC52a194acef951b3b36e94f294d836ae6'
auth_token = '988090f0870502e26899be8b5aeb41f0'
bot = TeleBot('873656324:AAFqF5d_0oAMgN2F2XPW5xMjrGULZvUnZTI')
keyboard1 = types.ReplyKeyboardMarkup()
keyboard1.row('Привет', 'Пока')
bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url="https://tel-bot-python.herokuapp.com/873656324:AAFqF5d_0oAMgN2F2XPW5xMjrGULZvUnZTI")
@app.route('/')
=======

server = flask.Flask(__name__)


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(flask.request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route('/', methods=["GET"])
>>>>>>> parent of efe5554... test
def index():
    """Return homepage."""
    json_data = {'Hello': 'World!'}
    # bot.remove_webhook()
    # bot.polling()
    return jsonify(json_data)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
        client = Client(account_sid, auth_token)
        call = client.calls.create(
            url='https://ex.ru',
            to='+79162721765',
            from_='+12027967603',
            timeout='60'
        )
        print(call.sid)


    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text.lower() == 'я тебя люблю':
        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')

@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)



if __name__ == "__main__":
<<<<<<< HEAD
    bot.remove_webhook()
    bot.polling()
    app.run()


=======
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
>>>>>>> parent of efe5554... test
