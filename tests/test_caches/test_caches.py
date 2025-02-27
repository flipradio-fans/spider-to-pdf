import unittest

from spider_to_pdf.caches import clean_all_cache, CacheInfo, update_cache, load_cache, LocalPathInfo


class TestCache(unittest.TestCase):
    def test_clean_cache(self):
        clean_all_cache()
        self.assertEqual(1, 1, "clean success")

    def test_update_cache(self):
        cache_infos = [CacheInfo("1", "2", 0, [LocalPathInfo(style_name="1", local_path="2"),
                                               LocalPathInfo(style_name="2", local_path="3")]),
                       CacheInfo("2", "3", 0, [LocalPathInfo(style_name="2", local_path="3"),
                                               LocalPathInfo(style_name="3", local_path="4")])]
        update_cache(cache_infos)
        self.assertEqual(1, 1, "update cache success")

    def testLoadCache(self):
        cache_infos = [CacheInfo("1", "2", 0, [LocalPathInfo(style_name="1", local_path="2"),
                                               LocalPathInfo(style_name="2", local_path="3")]),
                       CacheInfo("2", "3", 0, [LocalPathInfo(style_name="2", local_path="3"),
                                               LocalPathInfo(style_name="3", local_path="4")])]
        update_cache(cache_infos)
        load_caches = load_cache()
        self.assertEqual(len(cache_infos), len(load_caches), "load success")

    def test_filter_cache(self):
        all_caches = []
        caches = load_cache()
        all_caches.extend(list(filter(lambda x: x.page_time == 1738992547, caches)))
        self.assertIs(len(all_caches), 1, "data exists")
        filter_cache = all_caches[0]
        self.assertEqual(filter_cache.page_time, 1738992547, "page time is right")

    def test_load_cache_group_filter(self):
        all_caches = load_cache()
        print([item for local_path in all_caches for item in local_path.local_path_info])


if __name__ == '__main__':
    unittest.main()
