import telebot
from extensions import CryptoConverter, APIException
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['help', 'start'])
def welcome(message: telebot.types.Message):
    bot.reply_to(message, f"""Приветствую, я бот, который поможет тебе конвертировать валюту.\n
Для того, чтобы конвертировать валюту, нужно написать:\n
<название валюты, которую нужно конвертировать> <название валюты, в которую нужно конвертировать> и <количество первой валюты>""")

@bot.message_handler(commands=['values',])  
def values(message: telebot.types.Message):
    text = 'Доступные валюты: \n'

    for key in keys.keys():
        text = '\n'.join((text, key))

    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров')

        quote, base, amount = values
        total = CryptoConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода. \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} = {total}'
        bot.send_message(message.chat.id, text) 

bot.polling(none_stop=True)