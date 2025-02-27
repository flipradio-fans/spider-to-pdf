import unittest

from bs4 import BeautifulSoup

from spider_to_pdf.clean_pags import get_main_html_info, clean_html_info
from spider_to_pdf.spider_url import request_url


class TestSpider(unittest.TestCase):
    def test_get_main_html_info(self):
        html_soup = get_main_html_info(BeautifulSoup(request_url(
            "https://fearnation.club/xin-shi-pin-shi-jie-ku-cha-05yue-30ri-xin-wen-45tiao-ou-meng-jiang-qi-dong-wu-ke-lan-ru-meng-tan-pan/")))
        self.assertIsNotNone(html_soup, "crawl success.")

    def test_clean_html_info(self):
        html_soup = get_main_html_info(BeautifulSoup(request_url(
            "https://fearnation.club/xin-shi-pin-shi-jie-ku-cha-05yue-30ri-xin-wen-45tiao-ou-meng-jiang-qi-dong-wu-ke-lan-ru-meng-tan-pan/")))
        clean_html_info(html_soup)
        self.assertIsNotNone(html_soup, "clean success.")
        with open("test.html", "w+", encoding="UTF-8") as f:
            f.write(html_soup.prettify())


if __name__ == '__main__':
    unittest.main()
