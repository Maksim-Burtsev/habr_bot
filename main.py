import telebot
from telebot import types
from telegram import ParseMode

from parser import habr_parser_main

TOKEN = '5043259134:AAGSDHayOt-veEj_0MU5cQTX7ZveqjiT2-8'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("все публикации с главной страницы")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Привет', reply_markup=markup)

@bot.message_handler(content_types='text')
def foo(message):
    if message.text == 'все публикации с главной страницы':
        data = habr_parser_main()
        for i in data:
            # text = f'<a href={i[1]}>{i[0]}</a>'
            # bot.send_message(message.chat.id, text, parse_mode=ParseMode.HTML)
            bot.send_message(message.chat.id, i[1])

bot.infinity_polling()
