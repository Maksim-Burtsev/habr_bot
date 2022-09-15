import os

from telebot import TeleBot
from dotenv import load_dotenv

import services


load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = TeleBot(TOKEN)
parser = services.HabrParser()


@bot.message_handler(commands=["start"])
def start(message):
    markup = services.create_markup()
    bot.send_message(message.chat.id, "Привет", reply_markup=markup)


@bot.message_handler(content_types="text")
def get_articles(message):
    if message.text == "все публикации с главной страницы":
        articles = parser.get_articles()
        services.send_articles(bot, message, articles)

    elif message.text == "все посты за сегодня":
        articles = parser.get_today_articles()
        services.send_articles(bot, message, articles)


if __name__ == "__main__":
    bot.infinity_polling()
