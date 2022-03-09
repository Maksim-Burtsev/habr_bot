import re
import datetime
import requests

from bs4 import BeautifulSoup
import fake_useragent


URL = 'https://habr.com/ru/all/'


def get_articles_from_page(url) -> list:
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


def get_post_data(article) -> tuple:
    """Достаёт из поста всю необходимую информацию и упаковывает её для записи в БД"""

    try:
        title = article.find(
            'a', {'class': 'tm-article-snippet__title-link'}).text
    except:
        return False

    # time = datetime.datetime.strptime(
    #     article.find('time').get('title'),
    #     '%Y-%m-%d, %H:%M',
    # )

    time = article.find('time').get('title')[-5:]

    url = 'https://habr.com' + \
        article.find(
            'a', {'class': 'tm-article-snippet__title-link'}).get('href')

    return (title, url, time)


def habr_parser_main():
    """Основная функция программы"""

    URL = 'https://habr.com/ru/all/page'
    all_data = []

    for i in range(1, 2):
        url = URL + str(i) + '/'
        articles = get_articles_from_page(url)
        for j in range(len(articles)):
            data = get_post_data(articles[j])
            if data:
                all_data.append(data)

    return all_data


if __name__ == '__main__':
    ((habr_parser_main()))
