import time
from enum import Enum
from datetime import datetime, timezone, timedelta

import requests
import fake_useragent
from bs4 import BeautifulSoup
from telegram import ParseMode
from telebot import types, TeleBot
from pydantic.dataclasses import dataclass


class StatusCodeError(Exception):
    pass


class HtmlParseError(Exception):
    pass


class URL(str, Enum):
    HABR_DEFAULT = "https://habr.com"
    HABR_NEWS = "https://habr.com/ru/all/"


@dataclass
class Article:
    title: str
    url: str
    date: datetime

    @property
    def as_hypelink(self):
        return f'<a href="{self.url}">{self.title}</a>'

    def __repr__(self) -> str:
        return f"«{self.title}»"


def get_current_msk_date() -> str:
    """Return current date in Europe/Moscow."""
    delta = timedelta(hours=3, minutes=0)
    current_datetime = datetime.now(timezone.utc) + delta

    return str(current_datetime)[:10]  # 2022-03-10


def send_articles(
    bot: TeleBot, message: types.Message, articles: list[Article]
) -> None:
    """Send articles to user, 1 article = 1 message.

    Using sleep to slow sending."""
    for article in articles:
        time.sleep(0.333)
        bot.send_message(
            chat_id=message.chat.id, text=article.as_hypelink, parse_mode=ParseMode.HTML
        )


def create_markup() -> types.ReplyKeyboardMarkup:
    """Create buttons for menu"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("все публикации с главной страницы")
    item2 = types.KeyboardButton("все посты за сегодня")
    markup.add(item1)
    markup.add(item2)

    return markup


class HabrParser:
    def __init__(self) -> None:
        self.headers = {"user-agent": fake_useragent.UserAgent().random}

    def scrape_articles(self, url: str) -> list[BeautifulSoup | None]:
        """Get HTML page and return all articles blocks from it"""
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            return self.parse_page_articles(soup)
        raise StatusCodeError(
            f"Status code of response is {response.status_code} != 200"
        )

    def parse_page_articles(
        self, html_page: BeautifulSoup
    ) -> list[BeautifulSoup | None]:
        """Parse all articles from HTML page."""
        div = html_page.find("div", {"class": "tm-articles-subpage"})
        try:
            articles = div.find_all("article")
        except AttributeError as exc:
            raise HtmlParseError("Problem with parse urls from page.") from exc

        return articles

    def parse_article(self, article: BeautifulSoup) -> Article:
        """Parse article data and return it as HTML link"""
        try:
            title = article.find("a", {"class": "tm-article-snippet__title-link"}).text
            url = article.find("a", {"class": "tm-article-snippet__title-link"}).get(
                "href"
            )
            date = datetime.strptime(
                article.find("time").get("title"),
                "%Y-%m-%d, %H:%M",
            )
        except AttributeError as exc:
            raise HtmlParseError("Problem with parse article data") from exc

        return Article(title, URL.HABR_DEFAULT.value + url, date)

    def get_today_articles(self) -> list[Article]:
        """Return list of today's articles.

        Parse first three pages because to make sure no article was missed today."""
        articles = self.get_articles(pages_amount=3)
        current_date = get_current_msk_date()
        daily_articles = [
            article for article in articles if article.date == current_date
        ]

        return daily_articles

    def get_articles(self, pages_amount: int = 1) -> list[Article]:
        """Return reversed list of articles (from new to old).

        By default get articles from main page."""
        raw_articles = []
        for page_num in range(1, pages_amount + 1):
            url = f"{URL.HABR_NEWS.value}page{str(page_num)}/"
            raw_articles.extend(self.scrape_articles(url))

        articles = list(map(self.parse_article, raw_articles))

        return articles[::-1]


if __name__ == "__main__":
    pass
