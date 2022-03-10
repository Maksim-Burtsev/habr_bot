import datetime
import requests

from bs4 import BeautifulSoup
import fake_useragent


def get_current_date() -> str:
    """Возвращает текущую дату в MSK"""

    delta = datetime.timedelta(hours=3, minutes=0)

    current_datetime = datetime.datetime.now(datetime.timezone.utc) + delta

    return str(current_datetime)[:10]  # 2022-03-10


def get_articles_from_page(url: str) -> list[BeautifulSoup]:
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


def get_post_data(article: BeautifulSoup) -> tuple:
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


def habr_parser_main(pages_count: int) -> list:
    """Основная функция программы"""

    URL = 'https://habr.com/ru/all/page'
    all_data = []

    for i in range(1, pages_count+1):
        url = URL + str(i) + '/'
        articles = get_articles_from_page(url)
        for j in range(len(articles)):
            data = get_post_data(articles[j])
            if data:
                all_data.append(data)

    return all_data[::-1]


if __name__ == '__main__':
    habr_parser_main(1)
