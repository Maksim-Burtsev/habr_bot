import datetime
import requests

from bs4 import BeautifulSoup
import fake_useragent


class Parser:

    def __init__(self) -> None:
        self.url = 'https://habr.com/ru/all/'
        self.url_page = 'https://habr.com/ru/all/page'

    def _get_current_date(self) -> str:
        """Возвращает текущую дату в Europe/Moscow"""

        delta = datetime.timedelta(hours=3, minutes=0)

        current_datetime = datetime.datetime.now(datetime.timezone.utc) + delta

        return str(current_datetime)[:10]  # 2022-03-10

    def _get_articles_from_page(self, url: str) -> list[BeautifulSoup]:
        """Парсит все статьи со страницы"""

        user = fake_useragent.UserAgent().random
        header = {
            'user-agent': user,
        }

        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, 'lxml')

        div = soup.find('div', {'class': 'tm-articles-subpage'})

        articles = div.find_all('article')

        return articles

    def _get_post_data(self, article: BeautifulSoup) -> tuple:
        """Достаёт из поста заголовок, ссылку и время публикации и возвращает их"""

        try:
            title = article.find(
                'a', {'class': 'tm-article-snippet__title-link'}).text
        except:
            return False

        post_datetime = datetime.datetime.strptime(
            article.find('time').get('title'),
            '%Y-%m-%d, %H:%M',
        )

        date = str(post_datetime)[:10]  # 2022-03-10

        url = 'https://habr.com' + \
            article.find(
                'a', {'class': 'tm-article-snippet__title-link'}).get('href')

        return (title, url, date)

    def habr_parser_main(self, pages_count: int) -> list:
        """Основная функция программы"""

        all_data = []

        for i in range(1, pages_count+1):
            url = self.url_page + str(i) + '/'
            articles = self._get_articles_from_page(url)
            for j in range(len(articles)):
                data = self._get_post_data(articles[j])
                if data:
                    all_data.append(data)

        return all_data[::-1]


if __name__ == '__main__':
    parser = Parser()

    print(parser.habr_parser_main(1))
