import os

import telebot
from telebot import types
from telegram import ParseMode
from dotenv import load_dotenv

from parser import Parser


def send_hyperlink(bot: telebot.TeleBot, message: types.Message,
                   text: str, link: str) -> None:
    """Отправляет гиперссылку"""

    text = f'<a href="{link}">{text}</a>'
    bot.send_message(chat_id=message.chat.id,
                     text=text,
                     parse_mode=ParseMode.HTML)


load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)
parser = Parser()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("все публикации с главной страницы")
    item2 = types.KeyboardButton("все посты за сегодня")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, 'Привет', reply_markup=markup)


@bot.message_handler(commands=['10'])
def last_ten_posts(message):
    all_data = parser.habr_parser_main(1)
    for data in all_data[-10:]:
        send_hyperlink(bot, message, data[0], data[1])


@bot.message_handler(content_types='text')
def get_posts(message):
    if message.text == 'все публикации с главной страницы':
        all_data = parser.habr_parser_main(1)
        for data in all_data:
            send_hyperlink(bot, message, data[0], data[1])

    if message.text == "все посты за сегодня":
        all_data = parser.habr_parser_main(3)
        current_date = parser._get_current_date()
        for data in all_data:
            if data[2] == current_date:
                send_hyperlink(bot, message, data[0], data[1])


bot.infinity_polling()
