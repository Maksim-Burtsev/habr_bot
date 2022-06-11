import datetime
import requests
from typing import NamedTuple

import fake_useragent
from bs4 import BeautifulSoup


class PostDataTuple(NamedTuple):
    title: str
    url: str
    date: str


class Parser:

    def __init__(self) -> None:
        self.url = 'https://habr.com/ru/all/'
        self.url_page = 'https://habr.com/ru/all/page'
        self.user = fake_useragent.UserAgent().random

    def _get_current_date(self) -> str:
        """Возвращает текущую дату в Europe/Moscow"""

        delta = datetime.timedelta(hours=3, minutes=0)

        current_datetime = datetime.datetime.now(datetime.timezone.utc) + delta

        return str(current_datetime)[:10]  # 2022-03-10

    def _get_html_page(self, url: str) -> str:
        """
        Парсит html страницы
        """
        header = {'user-agent': self.user}
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response.text
        raise Exception('Parse error')

    def _get_articles_from_page(self, url: str) -> list[BeautifulSoup]:
        """Парсит все статьи со страницы"""

        html = self._get_html_page(url)
        soup = BeautifulSoup(html, 'lxml')

        div = soup.find('div', {'class': 'tm-articles-subpage'})
        articles = div.find_all('article')

        return articles

    def _get_post_data(self, article: BeautifulSoup) -> PostDataTuple:
        """
        Достаёт данные из html поста
        """
        try:
            title = article.find(
                'a', {'class': 'tm-article-snippet__title-link'}).text
        except:
            raise Exception('Проблемный пост')

        post_datetime = datetime.datetime.strptime(
            article.find('time').get('title'),
            '%Y-%m-%d, %H:%M',
        )

        date = str(post_datetime)[:10]  # 2022-03-10

        url = 'https://habr.com' + \
            article.find(
                'a', {'class': 'tm-article-snippet__title-link'}).get('href')

        return PostDataTuple(title=title, url=url, date=date)

    def habr_parser_main(self, pages_count: int) -> list[PostDataTuple]:
        """Основная функция программы"""

        all_articles = []

        for i in range(1, pages_count + 1):
            url_with_page = f'{self.url_page}{str(i)}/'
            articles = self._get_articles_from_page(url_with_page)
            all_articles.extend(articles)

        res = []
        for article in articles:
            data = self._get_post_data(article)
            if data:
                res.append(data)

        return res[::-1]


if __name__ == '__main__':
    parser = Parser()

    print(parser.habr_parser_main(1))
