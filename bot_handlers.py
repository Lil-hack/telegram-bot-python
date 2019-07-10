import types

from telegram import InputMediaDocument, InputMediaPhoto, InputMedia

from bot import bot # Импортируем объект бота
from messages import * # Инмпортируем все с файла сообщений
import json

@bot.message_handler(commands=['start']) # Выполняется, когда пользователь нажимает на start
def send_welcome(message):
    bot.send_message(message.chat.id, HELLO_MESSAGE)


@bot.message_handler(content_types=["text"]) # Любой текст
def repeat_all_messages(message):
    print(message)
    # bot.send_message(message.chat.id, message.text)

    with open('logo.png', 'rb') as f:
        # data = f.read()
        mes=bot.send_photo(message.chat.id,f)
        # bot.edit_message_media(media = types.InputMediaDocument(id='BQADAgADdwQAAjWfKUlb0KUllGBt4QI'),message.chat.id,1323)
        json_data = bot.forward_message(message.chat.id, message.chat.id, message.message_id+1)
        print(json_data.photo[0].file_id)
        bot.edit_message_media(InputMedia,message.chat.id,message.message_id+1)

    # bot.send_document(message.chat.id, open('data.json', 'rb'))
    json_data=bot.forward_message(message.chat.id,message.chat.id,1323)
    print(json_data)
    # bot.send_message(message.chat.id, data)
# bot.edit_message_media(media = types.InputMediaDocument(id='BQADAgADdwQAAjWfKUlb0KUllGBt4QI'),message.chat.id,1323)

if __name__ == '__main__':
    bot.polling(none_stop=True)