import unittest

from bs4 import BeautifulSoup

from spider_to_pdf.save_page import add_style, composite_template, style_list, init_title, save_page, \
    clean_page


class TestSavePage(unittest.TestCase):
    def test_style_list(self):
        self.assertEqual(len(style_list), 1, "style len is right")
        style_info = style_list[0]
        self.assertEqual(style_info.style_name, "dark", "style name is right")
        self.assertIsNotNone(style_info.home_page_path_soup, "home page path soup is not None")
        self.assertIsNotNone(style_info.base_template_path_soup, "base template path soup is not None")

    def test_composite_template(self):
        style_info = style_list[0]
        with open("test.html", "r", encoding="UTF-8") as f:
            main_html = BeautifulSoup(f.read(), "html.parser")
        main_html = composite_template(main_html, style_info)
        add_style(main_html, style_info)
        init_title(main_html)
        save_page(main_html, style_info.style_name, "test")
        self.assertEqual(1, 1, "save page succes")

    def test_clean_page(self):
        style_info = style_list[0]
        with open("test.html", "r", encoding="UTF-8") as f:
            main_html = BeautifulSoup(f.read(), "html.parser")
        save_page(main_html, style_info.style_name, "test")
        clean_page(style_info.style_name, "test")


if __name__ == '__main__':
    unittest.main()
