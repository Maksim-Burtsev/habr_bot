import os
import time

import telebot
from telebot import types
from telegram import ParseMode
from dotenv import load_dotenv

from services import get_current_msk_date, Article, HabrParser


load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
parser = HabrParser()


def send_articles(message: types.Message, articles: list[Article]) -> None:
    for article in articles:
        time.sleep(0.333)
        bot.send_message(
            chat_id=message.chat.id, text=article.as_hypelink, parse_mode=ParseMode.HTML
        )


def create_markup() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("все публикации с главной страницы")
    item2 = types.KeyboardButton("все посты за сегодня")
    markup.add(item1)
    markup.add(item2)

    return markup


@bot.message_handler(commands=["start"])
def start(message):
    markup = create_markup()
    bot.send_message(message.chat.id, "Привет", reply_markup=markup)


@bot.message_handler(content_types="text")
def get_articles(message):
    if message.text == "все публикации с главной страницы":
        articles = parser.get_articles(pages_amount=1)
        send_articles(message, articles)

    elif message.text == "все посты за сегодня":
        articles = parser.get_articles(pages_amount=3)
        current_date = get_current_msk_date()
        daily_articles = [
            article for article in articles if article.date == current_date
        ]
        send_articles(message, daily_articles)


if __name__ == "__main__":
    bot.infinity_polling()
