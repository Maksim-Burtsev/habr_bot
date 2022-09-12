import os

import telebot
from telebot import types
from telegram import ParseMode
from dotenv import load_dotenv

from parser import Parser


# TODO change link to URL
load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)
parser = Parser()


def send_hyperlink(
    bot: telebot.TeleBot, message: types.Message, text: str, link: str
) -> None:
    """Send hyperling"""

    text = f'<a href="{link}">{text}</a>'

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode=ParseMode.HTML)

#TODO crate markup maybe
def create_keyboard() -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("все публикации с главной страницы")
    item2 = types.KeyboardButton("все посты за сегодня")
    markup.add(item1)
    markup.add(item2)

    return markup


@bot.message_handler(commands=["start"])
def start(message):
    markup = create_keyboard()
    bot.send_message(message.chat.id, "Привет", reply_markup=markup)


@bot.message_handler(commands=["10"])
def last_ten_posts(message):
    posts = parser.habr_parser_main()
    # TODO send_posts
    for post in posts[-10:]:
        send_hyperlink(bot, message, post.title, post.url)


# TODO match case
@bot.message_handler(content_types="text")
def get_posts(message):
    if message.text == "все публикации с главной страницы":
        all_data = parser.habr_parser_main()
        # TODO send_data
        for data in all_data:
            send_hyperlink(bot, message, data[0], data[1])

    if message.text == "все посты за сегодня":
        posts = parser.habr_parser_main(3)
        current_date = parser._get_current_date()
        for post in posts:
            if post.date == current_date:
                send_hyperlink(bot, message, post.title, post.url)


if __name__ == "__main__":
    bot.infinity_polling()
