import unittest
import pytz
import datetime

from parser import Parser, PostDataTuple


class TestParser(unittest.TestCase):

    def setUp(self) -> None:

        self.parser = Parser()
        return super().setUp()

    def test_get_current_date(self):
        tz = pytz.timezone('Europe/Moscow')
        msk_now = datetime.datetime.now(tz)
        self.assertEqual(str(msk_now.date()), self.parser._get_current_date())

    def test_get_page_articles(self):
        articles = self.parser._get_articles_from_page()
        self.assertEqual(len(articles), 20)

    def test_get_post_data(self):
        article = self.parser._get_articles_from_page()[0]

        data = self.parser._get_post_data(article)

        self.assertEqual(type(data), PostDataTuple)
        self.assertEqual(len(data), 3)

    def test_paser_main(self):

        data = self.parser.habr_parser_main()

        self.assertEqual(len(data), 20)
        self.assertEqual(len(data[0]), 3)

    def test_paser_main_two_pages(self):

        data = self.parser.habr_parser_main(2)

        self.assertEqual(len(data), 40)
        self.assertEqual(len(data[0]), 3)