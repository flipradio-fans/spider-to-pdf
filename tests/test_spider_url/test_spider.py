import unittest

from spider_to_pdf.spider_url import download_ghost_blog_website_xml


class TestSpider(unittest.TestCase):
    def test_download_ghost_blog_website_xml(self):
        max_count = 0
        all_page_info = []
        for page_info in download_ghost_blog_website_xml("https://fearnation.club/sitemap-posts.xml"):
            if max_count == 10:
                break
            max_count += 1
            all_page_info.append(page_info)
        print(all_page_info)
        print([page.url for page in all_page_info])
        self.assertEqual(10, max_count, "crawl success.")


if __name__ == '__main__':
    unittest.main()
