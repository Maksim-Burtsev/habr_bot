import datetime
from enum import Enum
from typing import NamedTuple

import requests
import fake_useragent
from bs4 import BeautifulSoup


# TODO validation from pydantic maybe
class PostData(NamedTuple):
    title: str
    url: str
    date: str


# TODO maybe post init wich transfrom date


class URL(Enum, str):
    HABR_DEFAULT: str = "https://habr.com"
    HABR_NEWS: str = "https://habr.com/ru/all/"


def get_current_msk_date(self) -> str:
    """Return current date in Europe/Moscow."""
    delta = datetime.timedelta(hours=3, minutes=0)
    current_datetime = datetime.datetime.now(datetime.timezone.utc) + delta

    return str(current_datetime)[:10]  # 2022-03-10


class Parser:
    def __init__(self) -> None:
        self.headers = {"user-agent": fake_useragent.UserAgent().random}

    def get_articles(self, url: str) -> list[BeautifulSoup | None]:
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            return self.parse_page_articles(soup)
        # TODO custom exc
        raise Exception("Parse error")

    def parse_page_articles(
        self, html_page: BeautifulSoup
    ) -> list[BeautifulSoup | None]:
        """Parse all articles from html page."""
        try:
            div = html_page.find("div", {"class": "tm-articles-subpage"})
            articles = div.find_all("article")
        # AttributeError from exc
        except Exception as exc:
            pass

        return articles

    def clean_post_data(self, article: BeautifulSoup) -> PostData:
        """Parse post data."""
        try:
            title = article.find("a", {"class": "tm-article-snippet__title-link"}).text
            # TODO get_post_datetime
            post_datetime = datetime.datetime.strptime(
                article.find("time").get("title"),
                "%Y-%m-%d, %H:%M",
            )
            url = article.find("a", {"class": "tm-article-snippet__title-link"}).get(
                "href"
            )
        # TODO except what?
        except:
            raise Exception("")
        else:
            date = str(post_datetime)[:10]  # 2022-03-10
        # TODO never return empty named tuple, that's mean add validation, pydanctic maybe
        return PostData(title=title, url=URL.HABR_DEFAULT.value + url, date=date)

    # TODO rename
    def habr_parser_main(self, pages_count: int = 1) -> list[PostData]:
        raw_articles = []
        for page_num in range(1, pages_count + 1):
            url = f"{URL.HABR_NEWS.value}/page{str(page_num)}/"
            raw_articles.extend(self.get_articles(url))

        articles_data = list(map(self.clean_post_data, raw_articles))
        return articles_data[::-1]


if __name__ == "__main__":
    parser = Parser()

    print(parser.habr_parser_main(1))
