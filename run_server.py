import flask
from telebot import types
from config import *
from bot_handlers import bot
import os
from twilio.rest import Client
server = flask.Flask(__name__)
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say

response = VoiceResponse()
response.say('Hello World')

print(response)
account_sid = 'AC52a194acef951b3b36e94f294d836ae6'
auth_token = '988090f0870502e26899be8b5aeb41f0'
client = Client(account_sid, auth_token)
call = client.calls.create(
    url='https://raw.githubusercontent.com/akashkinKV/telegram-bot-python/master/test.xml',
    to='+79162721765',
    from_='+12027967603',
    timeout='15'
)
print(call.sid)
# message = client.messages.create(
#                      body="Join Earth's mightiest heroes. Like Kevin Bacon.",
#                      from_='+12027967603',
#                      to='+79162721765',
#
#                  )

# print(message.sid)
@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(flask.request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route('/', methods=["GET"])
def index():
    bot.remove_webhook()
    bot.set_webhook(url="https://{}.herokuapp.com/{}".format(APP_NAME, TOKEN))
    return "Hello from Heroku!", 200


if __name__ == "__main__":
    server.run(host="localhost", port=int(os.environ.get('PORT', 5000)))
    bot.remove_webhook()

    bot.set_webhook(url="https://ec2-18-184-5-216.eu-central-1.compute.amazonaws.comm/{}".format( TOKEN))