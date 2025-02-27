import unittest

from spider_to_pdf.convert_to_pdf import  add_page_numbers_with_outline
from spider_to_pdf.save_page import style_list


class TestPdfNumber(unittest.TestCase):

    def test_pdf_number_2(self):
        for style in style_list:
            add_page_numbers_with_outline("2023-06.pdf", "2023-06-02.pdf",style)


if __name__ == '__main__':
    unittest.main()
