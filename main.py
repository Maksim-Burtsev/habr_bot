import os

from dotenv import load_dotenv
import telebot
from telebot import types
from telegram import ParseMode

from parser import habr_parser_main

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("все публикации с главной страницы")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Привет', reply_markup=markup)


@bot.message_handler(content_types='text')
def foo(message):
    if message.text == 'все публикации с главной страницы':
        all_data = habr_parser_main()
        for data in all_data:
            text = f'<a href="{data[1]}">{data[0]}</a>'
            bot.send_message(chat_id=message.chat.id,
                             text=text,
                             parse_mode=ParseMode.HTML)


bot.infinity_polling()
