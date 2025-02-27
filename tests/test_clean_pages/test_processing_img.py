import unittest

from bs4 import BeautifulSoup

from spider_to_pdf.clean_pags import processing_ghost_blog_html_img, download_image


class TestSpider(unittest.TestCase):
    def test_download_image(self):
        result = download_image(
            "https://fearnation.club/content/images/size/w960/2024/05/photo_2024-05-29_13-26-25.jpg")
        self.assertEqual("../images/photo_2024-05-29_13-26-25.jpg", result, "images is error")

    def test_processing_ghost_blog_html_img(self):
        with open("test.html", "r", encoding="UTF-8") as f:
            html_soup = BeautifulSoup(f.read(), "html.parser")
            processing_ghost_blog_html_img(html_soup)
        self.assertEqual(1, 1, "over")


if __name__ == '__main__':
    unittest.main()
